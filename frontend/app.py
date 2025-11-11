"""Streamlit frontend for Voice Scam Detector"""
import streamlit as st
import requests
import os
import time
from typing import Dict
import plotly.graph_objects as go
from components.results import render_results
from components.batch import render_batch_processor
from utils.api_client import APIClient

# Page config
st.set_page_config(
    page_title="Voice Scam Detector",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .risk-critical {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .risk-high {
        background-color: #ff8800;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .risk-medium {
        background-color: #ffbb33;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .risk-low {
        background-color: #00C851;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize API client
api_client = APIClient()

# Header
st.markdown("""
    <div class="main-header">
        <h1>🔊 Voice Scam Detector</h1>
        <p>AI-Powered Deepfake Voice Detection</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This tool uses advanced AI to detect deepfake voices and potential scam calls.

    **Features:**
    - Real-time deepfake detection
    - Detailed confidence scoring
    - Suspicious segment analysis
    - Batch processing

    **Supported Formats:**
    MP3, WAV, M4A, OGG, FLAC
    """)

    st.divider()

    st.header("⚙️ Settings")
    sensitivity = st.select_slider(
        "Detection Sensitivity",
        options=["Low", "Medium", "High"],
        value="Medium"
    )

    show_advanced = st.checkbox("Show Advanced Details", value=False)

# Main content
tab1, tab2, tab3 = st.tabs(["📁 Single File", "📂 Batch Processing", "📊 Statistics"])

with tab1:
    st.subheader("Upload Audio File")

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="Maximum file size: 50MB"
    )

    if uploaded_file:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.audio(uploaded_file, format=f'audio/{uploaded_file.type.split("/")[1]}')

        with col2:
            st.write("**File Info:**")
            st.write(f"Name: {uploaded_file.name}")
            st.write(f"Size: {uploaded_file.size / 1024:.2f} KB")
            st.write(f"Type: {uploaded_file.type}")

        if st.button("🔍 Analyze Audio", type="primary", use_container_width=True):
            with st.spinner("Analyzing audio... This may take 10-30 seconds"):
                try:
                    result = api_client.analyze_audio(uploaded_file)

                    # Store result in session state
                    st.session_state['last_result'] = result

                    st.success("✅ Analysis Complete!")

                    # Display results
                    render_results(result, show_advanced)

                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")

with tab2:
    st.subheader("Batch Processing")
    st.write("Upload multiple files for batch analysis (max 10 files)")

    batch_files = st.file_uploader(
        "Choose audio files",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        accept_multiple_files=True
    )

    if batch_files:
        if len(batch_files) > 10:
            st.warning("⚠️ Maximum 10 files allowed. Only first 10 will be processed.")
            batch_files = batch_files[:10]

        st.write(f"📁 {len(batch_files)} files selected")

        if st.button("🔍 Analyze Batch", type="primary"):
            render_batch_processor(api_client, batch_files, show_advanced)

with tab3:
    st.subheader("Detection Statistics")

    if 'last_result' in st.session_state:
        result = st.session_state['last_result']

        # Confidence gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=result['confidence_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Deepfake Confidence"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 70], 'color': "yellow"},
                    {'range': [70, 90], 'color': "orange"},
                    {'range': [90, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        # Metadata
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Duration", f"{result['audio_metadata']['duration']:.2f}s")

        with col2:
            st.metric("Sample Rate", f"{result['audio_metadata']['sample_rate']} Hz")

        with col3:
            st.metric("Processing Time", f"{result['processing_time_ms']:.0f}ms")

    else:
        st.info("📊 Upload and analyze a file to see statistics")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Built for Tesonet AI Hackathon 2025 | Powered by Resemble AI</p>
        <p>⚠️ This tool is for demonstration purposes. Always verify critical decisions through multiple channels.</p>
    </div>
""", unsafe_allow_html=True)
