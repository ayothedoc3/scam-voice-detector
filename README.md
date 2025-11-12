# 🔊 Scam Shield - Voice Scam Detection Platform

Production-ready Progressive Web App for real-time voice deepfake detection and phone scam protection.

## Features

- ⚡ **Real-time call analysis** via Twilio Media Streams
- 🤖 **AI-powered deepfake detection** using Resemble AI
- 📱 **Progressive Web App** - installable, works offline
- 🔔 **Instant push notifications** when scams detected
- 📊 **Analytics and call history**
- 🔒 **Secure authentication**
- 🎯 **Voice analysis** with librosa
- 🌐 **WebSocket real-time updates**

## Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ↓
┌─────────────┐     WebSocket      ┌─────────────┐
│  Frontend   │ ←─────────────────→ │   Backend   │
│  (Next.js)  │                     │  (FastAPI)  │
└─────────────┘                     └──────┬──────┘
                                           │
                    ┌──────────────────────┼──────────────────┐
                    ↓                      ↓                   ↓
              ┌──────────┐          ┌──────────┐       ┌───────────┐
              │ Twilio   │          │ Resemble │       │PostgreSQL │
              │  Media   │          │    AI    │       │   Redis   │
              │ Streams  │          └──────────┘       └───────────┘
              └──────────┘
```

## Tech Stack

### Backend
- FastAPI 0.109+ (Python 3.11+)
- PostgreSQL 16 (SQLAlchemy async)
- Redis 7.2
- Socket.IO (WebSocket)
- Celery (background tasks)
- Twilio (Voice + Media Streams)
- Resemble AI (Deepfake detection)
- Librosa (Voice analysis)

### Frontend
- Next.js 14.2+ (App Router)
- TypeScript 5.3+
- TailwindCSS 3.4+
- shadcn/ui components
- Socket.io-client
- Zustand (state management)
- PWA support (next-pwa)

### Infrastructure
- Docker + Docker Compose
- Nginx (reverse proxy)
- MinIO (S3-compatible storage)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Twilio account with Voice API
- Resemble AI API key
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd scam-voice-detector
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` with your credentials:

```bash
# Twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Resemble AI
RESEMBLE_API_KEY=your_resemble_api_key

# Generate VAPID keys for push notifications
# npm install -g web-push
# web-push generate-vapid-keys
VAPID_PUBLIC_KEY=your_vapid_public_key
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_EMAIL=your_email@example.com
```

### 3. Start Services

```bash
# Build and start all services
make build
make up

# Run database migrations
make migrate

# View logs
make logs
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001

## Configuration

### Twilio Setup

1. Sign up at https://twilio.com
2. Get Account SID, Auth Token, and Phone Number
3. Configure webhooks in Twilio Console:
   - **Voice URL**: `https://yourdomain.com/api/v1/twilio/voice`
   - **Media Streams**: `wss://yourdomain.com/api/v1/twilio/media-stream`
   - **Status Callback**: `https://yourdomain.com/api/v1/twilio/status`

### Resemble AI Setup

1. Sign up at https://resemble.ai
2. Get API key from dashboard
3. Add to `.env` file

## Usage

### Protecting a Call

1. **Register/Login** to the application
2. Navigate to **Protect** page
3. Enter your phone number
4. Click **Start Protection**
5. Answer the incoming call from Scam Shield
6. Use your phone's "Add Call" feature to merge the suspicious caller
7. Watch the **real-time risk meter** update
8. Receive **instant alerts** if scam detected

### Uploading Audio Files

1. Navigate to **Upload** page
2. Select audio file (MP3, WAV, M4A, OGG, FLAC)
3. Wait for analysis
4. View risk score and detailed report

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
make test
```

## Project Structure

```
scam-shield/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── twilio/     # Twilio integration
│   │   │   ├── detection/  # Deepfake detection
│   │   │   └── audio/      # Voice analysis
│   │   ├── websocket/      # WebSocket server
│   │   ├── core/           # Auth & utilities
│   │   └── db/             # Database session
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js pages
│   │   ├── components/     # React components
│   │   ├── lib/            # Utilities & hooks
│   │   └── store/          # State management
│   └── package.json
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Protection
- `POST /api/v1/protection/start` - Start call protection

### Analysis
- `GET /api/v1/analysis/sessions` - Get call sessions
- `GET /api/v1/analysis/sessions/{id}` - Get session details
- `GET /api/v1/analysis/sessions/{id}/results` - Get analysis results

### Upload
- `POST /api/v1/upload/audio` - Upload audio file for analysis

### Twilio Webhooks
- `POST /api/v1/twilio/voice` - Voice webhook
- `POST /api/v1/twilio/media-stream` - Media stream webhook
- `POST /api/v1/twilio/status` - Status callback

## WebSocket Events

### Client → Server
- `join_call` - Join call room for updates
- `leave_call` - Leave call room

### Server → Client
- `connected` - Connection established
- `analysis_update` - Real-time analysis update
- `high_risk_alert` - High risk scam detected

## Production Deployment

### Environment Variables

Update `.env` for production:

```bash
# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=https://api.yourdomain.com

# Backend
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
SECRET_KEY=<strong-random-secret>
JWT_SECRET=<strong-random-jwt-secret>
CORS_ORIGINS=https://yourdomain.com

# App
APP_DOMAIN=yourdomain.com
APP_URL=https://api.yourdomain.com
```

### Deploy with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### SSL Configuration

Add SSL certificates to `nginx/ssl/` directory and update `nginx/nginx.conf`:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ...
}
```

## Monitoring

- **Health Check**: `GET /health`
- **Prometheus Metrics**: Available via prometheus-client
- **Logs**: `docker-compose logs -f`

## Troubleshooting

### Backend won't start
- Check `.env` file exists and has correct values
- Ensure PostgreSQL and Redis are running
- Run `docker-compose logs backend` for details

### Frontend won't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Ensure Nginx is properly routing requests

### Twilio webhooks not working
- Webhooks require public HTTPS URL
- Use ngrok for local testing: `ngrok http 8000`
- Update Twilio webhook URLs with ngrok URL

### WebSocket connection fails
- Ensure `/socket.io` path is accessible
- Check firewall allows WebSocket connections
- Verify Nginx WebSocket proxy configuration

## Make Commands

```bash
make build      # Build Docker images
make up         # Start all services
make down       # Stop all services
make logs       # View logs
make migrate    # Run database migrations
make test       # Run tests
make clean      # Clean up containers and volumes
```

## Security

- All API endpoints (except auth) require JWT authentication
- Passwords hashed with bcrypt
- HTTPS enforced in production
- CORS configured for allowed origins
- File upload size limits enforced
- SQL injection protection via SQLAlchemy
- Input validation with Pydantic

## License

MIT

## Team

Built for Tesonet AI Hackathon 2025
- **Ay**: API Integration
- **Raimy**: Backend Development
- **Sam**: Frontend Development

## Support

For issues and questions, please open a GitHub issue or contact the team.
