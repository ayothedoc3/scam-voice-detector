# 🛡️ Scam Shield Backend API

Production-ready FastAPI backend for real-time voice scam detection with Twilio integration, AI-powered deepfake detection, and WebSocket communication.

## 🚀 Features

- ✅ **Twilio Programmable Voice** - Conference bridge and media streaming
- ✅ **Resemble AI Integration** - Deepfake voice detection
- ✅ **Deepgram Integration** - Real-time speech-to-text
- ✅ **WebSocket Support** - Socket.IO for live updates
- ✅ **JWT Authentication** - Secure user authentication
- ✅ **PostgreSQL Database** - Async SQLAlchemy with Alembic migrations
- ✅ **Redis** - Caching and WebSocket state management
- ✅ **Docker Support** - Complete containerization
- ✅ **API Documentation** - Auto-generated OpenAPI docs

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

### API Keys Required

1. **Twilio**: Account SID, Auth Token, Phone Number
2. **Resemble AI**: API Key
3. **Deepgram**: API Key

## 🔧 Installation

### Option 1: Docker (Recommended)

```bash
# 1. Clone and navigate to backend
cd backend_new

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env and add your API keys
nano .env

# 4. Start all services
docker-compose up -d

# 5. Run database migrations
docker-compose exec api alembic upgrade head

# 6. View logs
docker-compose logs -f api
```

**Services will be available at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup PostgreSQL
createdb scamshield

# 4. Copy and configure environment
cp .env.example .env
# Edit .env with your configuration

# 5. Run migrations
alembic upgrade head

# 6. Start Redis
redis-server

# 7. Run the application
uvicorn app.main:socket_app --reload --host 0.0.0.0 --port 8000
```

## 🔐 Environment Configuration

Edit `.env` file:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/scamshield
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:password@localhost:5432/scamshield

# JWT Secret (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Twilio (Get from https://console.twilio.com)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Resemble AI (Get from https://app.resemble.ai)
RESEMBLE_API_KEY=your_resemble_api_key

# Deepgram (Get from https://console.deepgram.com)
DEEPGRAM_API_KEY=your_deepgram_api_key

# Redis
REDIS_URL=redis://localhost:6379/0

# Server
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 📡 API Endpoints

### Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Protection

```http
POST /api/v1/protection/start
POST /api/v1/protection/stop
GET  /api/v1/protection/status/{call_sid}
```

### Analysis

```http
GET /api/v1/analysis/history/{call_session_id}
GET /api/v1/analysis/sessions
```

### Twilio Webhooks

```http
POST /api/v1/twilio/voice/{call_session_id}
POST /api/v1/twilio/status/{call_session_id}
POST /api/v1/twilio/conference/{call_session_id}
POST /api/v1/twilio/media/{call_session_id}
```

## 🔌 WebSocket Events

Connect to: `ws://localhost:8000/socket.io/`

### Client → Server

```javascript
// Join call room
socket.emit('join_call', { call_sid: 'CAxxxx...' });

// Leave call room
socket.emit('leave_call', { call_sid: 'CAxxxx...' });
```

### Server → Client

```javascript
// Connection established
socket.on('connected', (data) => { });

// Real-time analysis update
socket.on('analysis_update', (data) => {
  // data.riskScore, data.riskLevel, data.deepfake, data.transcript
});

// Alternative event
socket.on('real_time_analysis', (data) => { });
```

## 🗄️ Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 🚀 Deployment

### Deploy to Render

1. **Create PostgreSQL database** on Render
2. **Create Redis instance** on Render
3. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `alembic upgrade head && uvicorn app.main:socket_app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables** (all from `.env.example`)
5. **Deploy**

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add -d postgres

# Add Redis
railway add -d redis

# Deploy
railway up
```

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create scamshield-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=ACxxxx...
heroku config:set TWILIO_AUTH_TOKEN=xxxxx
# ... (set all variables from .env.example)

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head
```

## 📦 Project Structure

```
backend_new/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # Authentication
│   │       │   ├── protection.py    # Protection endpoints
│   │       │   ├── twilio.py        # Twilio webhooks
│   │       │   └── analysis.py      # Analysis history
│   │       └── router.py
│   ├── core/
│   │   ├── config.py                # Settings
│   │   └── security.py              # JWT & auth
│   ├── db/
│   │   └── database.py              # Database setup
│   ├── models/                      # SQLAlchemy models
│   ├── schemas/                     # Pydantic schemas
│   ├── services/
│   │   ├── twilio_service.py        # Twilio integration
│   │   ├── resemble_service.py      # Deepfake detection
│   │   ├── deepgram_service.py      # Speech-to-text
│   │   ├── analysis_service.py      # AI analysis
│   │   └── socketio_service.py      # WebSocket
│   └── main.py                      # FastAPI app
├── alembic/                         # Database migrations
├── tests/                           # Test files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── .env.example
```

## 🔍 How It Works

### Call Flow

1. **User starts protection**
   ```
   Android App → POST /api/v1/protection/start
   ```

2. **Backend initiates Twilio call**
   ```
   Backend → Twilio: Create call to user's phone
   ```

3. **User answers, merges suspicious call**
   ```
   Twilio → POST /api/v1/twilio/conference/{id}
   ```

4. **Media streaming starts**
   ```
   Twilio → POST /api/v1/twilio/media/{id} (continuous)
   ```

5. **Real-time analysis**
   ```
   Backend: Audio → Resemble AI + Deepgram
   Backend: Calculate risk score
   Backend → WebSocket: Emit to Android app
   ```

6. **Android app receives updates**
   ```
   WebSocket → Android: Real-time risk meter updates
   ```

### Analysis Pipeline

```
Audio Chunk (Twilio Media Stream)
    ↓
Resemble AI (Deepfake Detection)
    ↓
Deepgram (Speech-to-Text)
    ↓
Analysis Service (Risk Calculation)
    ↓
Database (Save Result)
    ↓
WebSocket (Emit to Client)
```

## 🛠️ Development

### Run in Development Mode

```bash
# With auto-reload
uvicorn app.main:socket_app --reload --log-level debug

# View logs
tail -f logs/app.log
```

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Database Console

```bash
# Access PostgreSQL
docker-compose exec db psql -U postgres -d scamshield

# Or locally
psql scamshield
```

### Redis Console

```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# Or locally
redis-cli
```

## 🔒 Security Best Practices

1. **Never commit `.env`** - Keep credentials secure
2. **Use strong SECRET_KEY** - Generate with `openssl rand -hex 32`
3. **Enable HTTPS** in production
4. **Set CORS origins** - Don't use `*` in production
5. **Rate limiting** - Consider adding rate limits
6. **Input validation** - All inputs validated with Pydantic

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Logs

```bash
# Docker
docker-compose logs -f api

# Local
tail -f logs/app.log
```

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps db

# Check connection
psql -h localhost -U postgres -d scamshield
```

### Twilio Webhooks Not Working

1. **Check public URL** - Twilio needs public HTTPS URL
2. **Use ngrok** for local testing:
   ```bash
   ngrok http 8000
   ```
3. **Update Twilio webhooks** to ngrok URL

### WebSocket Connection Issues

1. **Check CORS settings** in `.env`
2. **Verify Socket.IO client** version compatibility
3. **Check network/firewall** settings

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Twilio Programmable Voice](https://www.twilio.com/docs/voice)
- [Socket.IO](https://socket.io/docs/v4/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License

---

**Built with FastAPI, Twilio, and AI-powered voice analysis** 🛡️
