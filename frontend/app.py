import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Scam Voice Detector", page_icon="🔊")

st.title("🔊 Voice Scam Detector")
st.write("Upload audio to detect AI-generated voice scams")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=['mp3', 'wav', 'm4a']
)

if uploaded_file:
    st.audio(uploaded_file)

    if st.button("Analyze Audio"):
        with st.spinner("Analyzing..."):
            # TODO: Send to backend
            backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

            files = {"file": uploaded_file}
            response = requests.post(f"{backend_url}/analyze", files=files)

            if response.ok:
                result = response.json()

                # Display results
                if result["is_scam"]:
                    st.error(f"⚠️ SCAM DETECTED ({result['confidence']:.1f}% confidence)")
                else:
                    st.success(f"✅ Likely Authentic ({result['confidence']:.1f}% confidence)")

                st.write(result["explanation"])
            else:
                st.error("Analysis failed. Try again.")
