import streamlit as st
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption


@st.cache_resource
def get_converter():
    """
    Initializes and caches the Docling DocumentConverter.
    This ensures models are only loaded once across app reruns.
    """
    return DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(
                enable_ocr=False
            )
        }
    )


def load_and_convert_cv(file_path: str) -> str:
    """
    Converts a PDF/DOCX file to Markdown format using Docling.
    
    Args:
        file_path (str): The local path to the uploaded CV file.
        
    Returns:
        str: The converted markdown text.
    """
    converter = get_converter()
    result = converter.convert(file_path)
    text_content = result.document.export_to_text()
    return text_content
