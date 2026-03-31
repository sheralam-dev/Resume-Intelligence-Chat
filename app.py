import streamlit as st
import pandas as pd
import tempfile

from core.ingestion.docling_loader import load_and_convert_cv
from core.parsing.extractor import extract_resume
from core.processing.dataframe import resume_to_df

st.title("CV Analyzer")

# ---- session state init ----
if "processed" not in st.session_state:
    st.session_state.processed = False
if "df" not in st.session_state:
    st.session_state.df = None

uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

if st.button("Upload New CV"):
    st.session_state.processed = False
    st.session_state.df = None

# ---- process only once ----
if uploaded_file and not st.session_state.processed:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    text = load_and_convert_cv(pdf_path)
    data = extract_resume(text)
    df = resume_to_df(data)

    st.session_state.df = df
    st.session_state.processed = True

# ---- display from session (no recompute) ----
if st.session_state.processed and st.session_state.df is not None:
    df = st.session_state.df

    st.subheader("Extracted Data")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="cv_data.csv",
        mime="text/csv"
    )