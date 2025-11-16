"""Results visualization component"""
import streamlit as st
from typing import Dict

def render_results(result: Dict, show_advanced: bool = False):
    """Render detection results with visualizations"""

    # Risk level banner
    risk_level = result['risk_level']
    confidence = result['confidence_score']

    risk_class = f"risk-{risk_level.lower()}"

    if result['is_deepfake']:
        emoji = "🚨" if risk_level == "CRITICAL" else "⚠️"
        st.markdown(f"""
            <div class="{risk_class}">
                {emoji} DEEPFAKE DETECTED - {risk_level} RISK ({confidence:.1f}% confidence)
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="risk-low">
                ✅ AUTHENTIC AUDIO - LOW RISK ({confidence:.1f}% confidence)
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Explanation
    st.subheader("📋 Analysis Summary")
    st.write(result['explanation'])

    # Suspicious segments
    if result.get('suspicious_segments'):
        st.subheader("🔍 Suspicious Segments Detected")

        for idx, segment in enumerate(result['suspicious_segments'], 1):
            with st.expander(f"Segment {idx}: {segment['start_time']:.1f}s - {segment['end_time']:.1f}s"):
                st.write(f"**Confidence:** {segment['confidence']:.1f}%")
                st.write(f"**Reason:** {segment['reason']}")
                if segment.get('features_detected'):
                    st.write(f"**Features:** {', '.join(segment['features_detected'])}")

    # Advanced details
    if show_advanced:
        st.subheader("🔬 Technical Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Audio Metadata:**")
            metadata = result['audio_metadata']
            st.json({
                "Duration": f"{metadata['duration']:.2f}s",
                "Sample Rate": f"{metadata['sample_rate']} Hz",
                "Channels": metadata['channels'],
                "Format": metadata['format']
            })

        with col2:
            st.write("**Detection Details:**")
            st.json({
                "Processing Time": f"{result['processing_time_ms']:.0f}ms",
                "Analysis Timestamp": result['analysis_timestamp'],
                "Risk Level": result['risk_level']
            })
