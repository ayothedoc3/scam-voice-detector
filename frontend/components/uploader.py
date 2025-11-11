"""File upload component"""
import streamlit as st

def render_file_uploader():
    """Render file upload interface"""
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="Maximum file size: 50MB"
    )
    
    return uploaded_file
