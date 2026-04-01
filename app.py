import streamlit as st
import pandas as pd
import tempfile

from core.ingestion.docling_loader import load_and_convert_cv
from core.parsing.extractor import extract_resume
from core.processing.dataframe import resume_to_df, resume_to_dfs

st.title("📊 Resume Data Extractor")

# ---- session state init ----
if "processed" not in st.session_state:
    st.session_state.processed = False
if "dfs" not in st.session_state:
    st.session_state.dfs = None

uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])


if not uploaded_file:
    st.session_state.processed = False
    st.session_state.dfs = None


# ---- process only once ----
if uploaded_file and not st.session_state.processed:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    text = load_and_convert_cv(pdf_path)
    data = extract_resume(text)
    dfs = resume_to_dfs(data)

    st.session_state.data = data
    st.session_state.dfs = dfs
    st.session_state.processed = True

# ---- display from session (no recompute) ----
if st.session_state.processed and st.session_state.dfs is not None:
    dfs = st.session_state.dfs
    data = st.session_state.data # Ensure data is pulled from state

    
    # Extract row from 'base' dataframe (assuming it's a single-row DF)
    base_data = dfs['base'].iloc[0]
    

    st.subheader("Candidate Profile")
    col_spacer, col_content = st.columns([0.01, 0.99])
    with col_content:
        st.write(f"**Name:** {base_data.get('full_name', 'N/A')}")
        
        # Iterate through contact fields (the ones prefixed with contact_)
        contact_fields = {k.replace("contact_", "").title(): v for k, v in base_data.items() if k.startswith("contact_") and v}
        for label, value in contact_fields.items():
            st.write(f"**{label}:** {value}")

        st.write(f"**AI/ML Skills:** {base_data.get('ai_ml_skills') or 'N/A'}")
        st.write(f"**Technical Skills:** {base_data.get('technical_skills') or 'N/A'}")
        st.write(f"**Certifications:** {base_data.get('certifications') or 'N/A'}")
        
        if base_data.get("summary"):
            st.info(f"**Summary:** {base_data['summary']}")


    # Display other tables (Experience, Education, etc.)
    for label, df in dfs.items():
        if label == "base":
            continue 
        st.subheader(label.replace("_", " ").title())
        st.dataframe(df, use_container_width=True)

    # Download Button
    df_full = resume_to_df(data)
    csv = df_full.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name=f"analyzed_{uploaded_file.name}.csv",
        mime="text/csv"
    )




# "full_name": r.get("full_name"),
# "summary": r.get("summary"),
# **{f"contact_{k}": v for k, v in (r.get("contact") or {}).items()},
# "ai_ml_skills"
# "technical_skills"
# "certifications"