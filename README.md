# 🔊 Voice Scam Detector

AI-powered voice deepfake detection system built for the Tesonet AI Hackathon 2025. Detects AI-generated voice scams using Resemble AI's detection API.

## 🎯 Project Overview

Voice Scam Detector is a production-ready web application that analyzes audio files to identify deepfake voices commonly used in scam attempts. The system provides:

- **Real-time Detection**: Fast analysis of audio files (10-30 seconds)
- **Detailed Analysis**: Confidence scores, risk levels, and suspicious segment identification
- **Batch Processing**: Analyze up to 10 files simultaneously
- **Interactive UI**: User-friendly Streamlit interface with visualizations
- **Production Ready**: Containerized, scalable, and deployable

## 🏗️ Architecture

### Tech Stack

- **Backend**: Python 3.11 + FastAPI
- **Frontend**: Streamlit
- **AI Detection**: Resemble AI Detect API
- **Audio Processing**: librosa, pydub, soundfile
- **Deployment**: Docker, Render (backend), Streamlit Cloud (frontend)

### System Flow

```
User Upload → Validation → Audio Preprocessing → Resemble AI API → 
Results Processing → Risk Assessment → Visualization
```

## 📁 Project Structure

```
scam-voice-detector/
├── backend/
│   ├── app/
│   │   ├── services/          # Core business logic
│   │   ├── api/               # FastAPI routes
│   │   ├── utils/             # Utilities and helpers
│   │   ├── config.py          # Configuration management
│   │   ├── models.py          # Pydantic models
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Unit tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── components/            # UI components
│   ├── utils/                 # Frontend utilities
│   ├── app.py                 # Streamlit application
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Resemble AI API key ([Get one here](https://www.resemble.ai/))
- FFmpeg (for audio processing)

### Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/ayothedoc3/scam-voice-detector.git
cd scam-voice-detector
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your RESEMBLE_API_KEY

# Run the backend
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

#### 3. Frontend Setup

```bash
cd ../frontend

# Create virtual environment (if not already)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Set BACKEND_URL=http://localhost:8000

# Run the frontend
streamlit run app.py
```

Frontend will be available at: http://localhost:8501

### Docker Deployment

```bash
# Set your API key in environment
export RESEMBLE_API_KEY=your_api_key_here

# Build and run with Docker Compose
docker-compose up --build

# Access the applications:
# Backend: http://localhost:8000
# Frontend: http://localhost:8501
```

## 📖 API Documentation

### Endpoints

#### `POST /api/v1/analyze`
Analyze a single audio file for deepfake detection.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@audio.mp3"
```

**Response:**
```json
{
  "is_deepfake": true,
  "confidence_score": 87.5,
  "risk_level": "HIGH",
  "explanation": "High confidence (87.5%) of AI-generated voice detected...",
  "suspicious_segments": [
    {
      "start_time": 2.5,
      "end_time": 5.0,
      "confidence": 92.3,
      "reason": "Synthetic voice patterns detected",
      "features_detected": ["pitch_anomaly", "spectral_artifacts"]
    }
  ],
  "audio_metadata": {
    "filename": "audio.mp3",
    "duration": 15.3,
    "sample_rate": 44100,
    "channels": 2,
    "format": "mp3"
  },
  "processing_time_ms": 1234.5
}
```

#### `POST /api/v1/analyze/batch`
Analyze multiple audio files (max 10).

#### `GET /api/v1/health`
Health check endpoint.

## 🎨 Features

### Single File Analysis
- Upload audio files (MP3, WAV, M4A, OGG, FLAC)
- Real-time analysis with progress indicators
- Detailed results with risk level visualization
- Audio playback integration

### Batch Processing
- Upload up to 10 files simultaneously
- Progress tracking for each file
- Batch statistics and summary
- Individual file result inspection

### Advanced Detection
- AI-powered deepfake detection via Resemble AI
- Suspicious segment identification
- Confidence scoring (0-100%)
- Risk level classification (LOW, MEDIUM, HIGH, CRITICAL)

### Visualization
- Interactive confidence gauge
- Risk level color coding
- Audio metadata display
- Processing time metrics

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

## 🚢 Deployment

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `RESEMBLE_API_KEY`
5. Deploy

### Frontend (Streamlit Cloud)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app pointing to `frontend/app.py`
4. Add secret: `BACKEND_URL` (your Render backend URL)
5. Deploy

### Alternative: VPS/Cloud

Use the provided `docker-compose.yml` for easy deployment on any VPS:

```bash
# On your server
git clone <repo>
cd scam-voice-detector
export RESEMBLE_API_KEY=your_key
docker-compose up -d
```

## 🔐 Security Considerations

- API keys stored in environment variables (never in code)
- File size limits enforced (50MB max)
- File type validation
- Temporary file cleanup
- CORS configuration for production
- Rate limiting support

## 📊 Performance

- Average analysis time: 10-30 seconds per file
- Supports files up to 50MB
- Batch processing: up to 10 files
- Concurrent request handling via FastAPI

## 🛠️ Configuration

### Backend Environment Variables

```env
RESEMBLE_API_KEY=your_api_key_here
APP_NAME=Voice Scam Detector API
DEBUG=false
MAX_FILE_SIZE=52428800
CORS_ORIGINS=["*"]
```

### Frontend Environment Variables

```env
BACKEND_URL=http://localhost:8000
```

## 🤝 Contributing

This project was built for the Tesonet AI Hackathon 2025. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 👥 Team

Built with ❤️ for the Tesonet AI Hackathon 2025

## 🙏 Acknowledgments

- **Resemble AI** for their powerful deepfake detection API
- **Tesonet** for hosting the hackathon
- **FastAPI** and **Streamlit** communities

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Contact: [Your Contact Info]

## 🔗 Links

- [Resemble AI Documentation](https://www.resemble.ai/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**⚠️ Disclaimer**: This tool is for demonstration and educational purposes. Always verify critical security decisions through multiple channels and professional security services.
