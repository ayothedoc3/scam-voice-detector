"""Batch processing component"""
import streamlit as st
from typing import List
import time

def render_batch_processor(api_client, files: List, show_advanced: bool = False):
    """Render batch processing interface and results"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Uploading files for batch analysis...")
        
        # Call batch API
        result = api_client.analyze_batch(files)
        
        progress_bar.progress(100)
        status_text.text("✅ Batch analysis complete!")
        
        # Display summary
        st.subheader("📊 Batch Analysis Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Files", result['total_files'])
        
        with col2:
            st.metric("Processed", result['processed'])
        
        with col3:
            st.metric("Failed", result['failed'])
        
        with col4:
            st.metric("Total Time", f"{result['processing_time_total_ms']:.0f}ms")
        
        st.divider()
        
        # Display individual results
        st.subheader("📁 Individual Results")
        
        for idx, file_result in enumerate(result['results'], 1):
            with st.expander(f"File {idx}: {file_result['audio_metadata']['filename']}", expanded=False):
                from components.results import render_results
                render_results(file_result, show_advanced)
        
        # Statistics
        if result['results']:
            st.subheader("📈 Batch Statistics")
            
            deepfake_count = sum(1 for r in result['results'] if r['is_deepfake'])
            authentic_count = len(result['results']) - deepfake_count
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Deepfakes Detected", deepfake_count)
            
            with col2:
                st.metric("Authentic Files", authentic_count)
            
            # Risk level breakdown
            risk_levels = {}
            for r in result['results']:
                risk = r['risk_level']
                risk_levels[risk] = risk_levels.get(risk, 0) + 1
            
            st.write("**Risk Level Distribution:**")
            for risk, count in sorted(risk_levels.items()):
                st.write(f"- {risk}: {count} files")
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Batch analysis failed: {str(e)}")
