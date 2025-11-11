from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from detector import VoiceDetector

app = FastAPI(title="Scam Voice Detector API")

# CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = VoiceDetector()

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """Analyze uploaded audio for deepfake/scam indicators"""

    if not file.filename.endswith(('.mp3', '.wav', '.m4a')):
        raise HTTPException(400, "Unsupported file format")

    # Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = detector.analyze(temp_path)
        return result
    finally:
        os.remove(temp_path)

@app.get("/health")
def health_check():
    return {"status": "ok"}
