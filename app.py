import ast

import streamlit as st
import tempfile
import os

from core.chains import generate_sql_query, generate_nl_answer
from core.ingestion.docling_loader import load_and_convert_cv
from core.parsing.extractor import extract_resume
from core.parsing.schema import Resume
from core.processing.database import resume_to_sqlite
from langchain_community.utilities import SQLDatabase


@st.cache_resource
def get_db():
    return SQLDatabase.from_uri("sqlite:///data/db/resumes.db")

st.set_page_config(page_title="Resume AI Assistant", layout="wide")
st.title("🤖 Resume Intelligence Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for File Uploads
with st.sidebar:
    st.header("Upload Center")
    uploaded_files = st.file_uploader(
        "Upload PDF Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Process & Index Resumes"):
        os.makedirs("data/db", exist_ok=True)
        with st.spinner(f"Indexing {len(uploaded_files)} resumes..."):
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    pdf_path = tmp.name
                try:
                    text = load_and_convert_cv(pdf_path)
                    data: Resume = extract_resume(text)
                    resume_to_sqlite(data, "data/db/resumes.db")
                finally:
                    os.remove(pdf_path)
        st.success("Indexing complete!")

    st.divider()

    confirm = st.checkbox("Confirm delete database")
    # DELETE DB BUTTON
    if st.button("🗑️ Delete Database"):
        if confirm:
            tables = get_db().run("select name from sqlite_master where type='table';")
            # tables = "[('resume_base',), ('contact',), ('certifications',), ('education',), ('experience',), ('projects',)]"
            tables = ast.literal_eval(tables)
            for table in tables:
                get_db().run(f"drop table if exists {table[0]};")
            st.success("All tables dropped successfully.")
        else:
            st.warning("Please confirm deletion first.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask about your resumes (e.g., 'List all candidates names')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing database..."):
            try:
                # create sql query for the user query
                sql_query = generate_sql_query(prompt).strip()
                # sql_query = "select name from resume_base;" # fake query
                print('sql_query: ', sql_query)
                if sql_query == "IRRELEVANT QUERY":
                    response = "This question is outside the resume database scope."
                elif not sql_query.upper().startswith(("SELECT", "WITH")):
                    raise ValueError("Invalid SQL generated")
                else:
                    db_result = get_db().run(sql_query)
                    if not db_result:
                        db_result = "NO_DATA"
                    # create a natural language response based on db results. 
                    response = generate_nl_answer(prompt, db_result)
                    # response = db_result # fake response
                    print('response generated')
                st.markdown(response)
                st.code(sql_query, language="sql", width="content")  # show query
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I ran into an error: {str(e)}"
                st.error(error_msg)
