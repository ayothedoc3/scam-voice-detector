# Project Structure

```
scam-voice-detector/
│
├── 📄 README.md                    # Comprehensive project documentation
├── 📄 .gitignore                   # Git ignore rules
├── 📄 docker-compose.yml           # Docker orchestration
│
├── 🔧 backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration management
│   │   ├── models.py               # Pydantic data models
│   │   │
│   │   ├── api/                    # API layer
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # API endpoints
│   │   │   └── dependencies.py     # Dependency injection
│   │   │
│   │   ├── services/               # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py         # Main analysis orchestrator
│   │   │   ├── audio_processor.py  # Audio preprocessing
│   │   │   └── detector.py         # Resemble AI integration
│   │   │
│   │   └── utils/                  # Utilities
│   │       ├── __init__.py
│   │       ├── errors.py           # Custom exceptions
│   │       └── logger.py           # Logging configuration
│   │
│   ├── tests/                      # Test suite
│   │   ├── __init__.py
│   │   ├── test_api.py            # API endpoint tests
│   │   ├── test_detector.py       # Detector tests
│   │   ├── test_audio_processor.py # Audio processor tests
│   │   └── sample_audio/          # Test audio files
│   │
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Docker image configuration
│   ├── render.yaml                 # Render.com deployment config
│   └── .env.example                # Environment variables template
│
└── 🎨 frontend/                    # Streamlit Frontend
    ├── app.py                      # Main Streamlit application
    ├── config.py                   # Frontend configuration
    │
    ├── components/                 # UI components
    │   ├── __init__.py
    │   ├── results.py              # Results visualization
    │   ├── batch.py                # Batch processing UI
    │   └── uploader.py             # File upload component
    │
    ├── utils/                      # Frontend utilities
    │   ├── __init__.py
    │   └── api_client.py           # Backend API client
    │
    ├── requirements.txt            # Python dependencies
    ├── Dockerfile                  # Docker image configuration
    └── .env.example                # Environment variables template
```

## File Descriptions

### Backend Core Files

- **main.py**: FastAPI application initialization, CORS, and route registration
- **config.py**: Settings management using Pydantic Settings
- **models.py**: Data validation models for requests and responses

### Backend Services

- **analyzer.py**: Main orchestration - coordinates detection pipeline
- **audio_processor.py**: Audio validation, normalization, and preprocessing
- **detector.py**: Resemble AI API integration and result parsing

### Backend API

- **routes.py**: API endpoints for single/batch analysis and health checks
- **dependencies.py**: Dependency injection helpers

### Frontend Components

- **app.py**: Main Streamlit interface with tabs and layout
- **results.py**: Renders detection results with visualizations
- **batch.py**: Batch processing interface and progress tracking
- **uploader.py**: File upload component

### Frontend Utils

- **api_client.py**: HTTP client for backend communication

## Key Features by File

| File | Key Features |
|------|--------------|
| `analyzer.py` | Pipeline orchestration, timing, error handling |
| `detector.py` | Risk calculation, explanation generation, API calls |
| `audio_processor.py` | Format conversion, normalization, metadata extraction |
| `routes.py` | File validation, temp file handling, batch processing |
| `results.py` | Risk visualization, segment display, metadata rendering |
| `batch.py` | Progress tracking, batch statistics, result aggregation |

## Technology Stack

- **Backend**: FastAPI, Uvicorn, Pydantic, librosa, pydub
- **Frontend**: Streamlit, Plotly, requests
- **AI**: Resemble AI Detect API
- **Testing**: pytest, httpx
- **Deployment**: Docker, Render, Streamlit Cloud
