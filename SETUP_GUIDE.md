# 🚀 Quick Setup Guide

## Prerequisites Checklist

- [ ] Python 3.11 or higher installed
- [ ] Git installed
- [ ] Resemble AI API key obtained
- [ ] (Optional) Docker and Docker Compose installed

## Setup Steps

### Step 1: Get Resemble AI API Key

1. Visit [Resemble AI](https://www.resemble.ai/)
2. Sign up for an account
3. Navigate to API settings
4. Generate an API key for the Detect API
5. Save this key securely

### Step 2: Clone and Setup Project

```bash
# Navigate to project directory
cd scam-voice-detector

# Verify project structure
ls -la

# You should see:
# backend/
# frontend/
# docker-compose.yml
# README.md
```

### Step 3: Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor

# Add your Resemble API key:
# RESEMBLE_API_KEY=your_actual_api_key_here

# Test the installation
python -c "from app.main import app; print('Backend imports successful!')"
```

### Step 4: Frontend Setup

```bash
# Open a new terminal
cd scam-voice-detector/frontend

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit if needed (default localhost:8000 should work)
# BACKEND_URL=http://localhost:8000
```

### Step 5: Running the Application

#### Option A: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd scam-voice-detector/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd scam-voice-detector/frontend
source venv/bin/activate
streamlit run app.py
```

#### Option B: Docker (Recommended for Production)

```bash
# From project root
cd scam-voice-detector

# Set your API key
export RESEMBLE_API_KEY=your_actual_api_key_here

# Build and run
docker-compose up --build

# To run in background:
docker-compose up -d

# To stop:
docker-compose down
```

### Step 6: Verify Installation

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "Voice Scam Detector API",
     "version": "1.0.0"
   }
   ```

2. **Frontend Access:**
   - Open browser to http://localhost:8501
   - You should see the Voice Scam Detector interface

3. **API Documentation:**
   - Visit http://localhost:8000/docs
   - Interactive Swagger UI should be visible

### Step 7: Test with Sample Audio

1. Prepare a test audio file (MP3, WAV, etc.)
2. Upload via the Streamlit interface
3. Click "Analyze Audio"
4. Wait for results (10-30 seconds)

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
# Make sure you activated the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**2. "Permission denied" on port 8000 or 8501**
```bash
# Use different ports
uvicorn app.main:app --port 8001  # Backend
streamlit run app.py --server.port 8502  # Frontend
```

**3. "Resemble API key not found"**
```bash
# Verify .env file exists and has the key
cat backend/.env

# Should contain:
# RESEMBLE_API_KEY=your_key_here
```

**4. FFmpeg not found**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

**5. Docker issues**
```bash
# Check Docker is running
docker --version
docker-compose --version

# Rebuild without cache
docker-compose build --no-cache
docker-compose up
```

## Running Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with output
pytest -v

# Run with coverage
pytest --cov=app tests/
```

## Environment Variables Reference

### Backend (.env)
```env
RESEMBLE_API_KEY=your_key_here          # Required
DEBUG=false                              # Optional: true for dev
MAX_FILE_SIZE=52428800                  # Optional: 50MB default
CORS_ORIGINS=["*"]                      # Optional: adjust for production
```

### Frontend (.env)
```env
BACKEND_URL=http://localhost:8000       # Required
```

## Next Steps

1. **Test the system** with various audio files
2. **Review API documentation** at http://localhost:8000/docs
3. **Customize settings** in config files as needed
4. **Deploy to production** using deployment guides in README.md

## Support

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review logs in the terminal
3. Verify all prerequisites are installed
4. Check the main README.md for detailed documentation

## Security Notes

- Never commit `.env` files to Git
- Keep your Resemble API key secure
- For production, set `DEBUG=false`
- Configure CORS properly for production deployments
- Use environment-specific configuration

---

**Ready to detect voice scams!** 🎯
