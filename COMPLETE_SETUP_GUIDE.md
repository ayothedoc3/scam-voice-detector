# 🛡️ Scam Shield - Complete Setup Guide

**Production-ready voice scam detection system with Android app + FastAPI backend**

## 🎯 What You Have Now

✅ **Native Android App** (Kotlin + Jetpack Compose)
✅ **FastAPI Backend** (Python with Twilio, AI integration)
✅ **Real-time Communication** (WebSocket/Socket.IO)
✅ **AI-Powered Analysis** (Resemble AI + Deepgram)
✅ **Cloud-Ready** (Docker + deployment guides)

---

## 📋 Prerequisites Checklist

### Services to Sign Up For:

1. **Twilio** (Voice calling) - https://www.twilio.com/try-twilio
   - Free trial: $15 credit
   - Cost: ~$1/month for phone number + usage

2. **Resemble AI** (Deepfake detection) - https://app.resemble.ai
   - Sign up for API access
   - Get API key from dashboard

3. **Deepgram** (Speech-to-text) - https://console.deepgram.com
   - Free tier available
   - Create API key

4. **Firebase** (Push notifications) - https://console.firebase.google.com
   - Create new project
   - Add Android app
   - Download google-services.json

### Development Tools:

- **For Backend**: Docker + Docker Compose (or Python 3.11+)
- **For Android**: Android Studio Hedgehog+
- **Optional**: ngrok (for local Twilio testing)

---

## 🚀 Quick Start (Fastest Path)

### Step 1: Get API Keys (10 minutes)

```bash
# Get these ready:
TWILIO_ACCOUNT_SID=ACxxxxxxxx...
TWILIO_AUTH_TOKEN=xxxxx...
TWILIO_PHONE_NUMBER=+1234567890
RESEMBLE_API_KEY=xxxxx...
DEEPGRAM_API_KEY=xxxxx...
```

See `backend_new/QUICKSTART.md` for detailed instructions on getting each key.

### Step 2: Start Backend (5 minutes)

```bash
cd backend_new

# Copy environment file
cp .env.example .env

# Edit .env and paste your API keys
nano .env

# Start with Docker
docker-compose up -d

# Initialize database
docker-compose exec api alembic upgrade head

# Verify it's running
curl http://localhost:8000/health
```

**✅ Backend running at http://localhost:8000**

### Step 3: Get Backend URL

**Option A: Local Testing**
```bash
# Find your computer's IP address
ifconfig  # Mac/Linux
ipconfig  # Windows

# Your backend URL will be:
http://YOUR_IP_ADDRESS:8000
```

**Option B: Deploy to Cloud (Recommended)**
```bash
# Deploy to Render, Railway, or Heroku
# See backend_new/README.md for deployment guides

# You'll get a URL like:
https://your-app.onrender.com
```

### Step 4: Configure Android App (5 minutes)

```bash
cd ScamShieldAndroid

# 1. Add your Firebase config
# Replace app/google-services.json with your file from Firebase

# 2. Update API URLs in app/build.gradle.kts
```

Edit `app/build.gradle.kts`:
```kotlin
// For local testing (emulator):
buildConfigField("String", "API_BASE_URL", "\"http://10.0.2.2:8000\"")
buildConfigField("String", "WS_BASE_URL", "\"ws://10.0.2.2:8000\"")

// For local testing (physical device):
buildConfigField("String", "API_BASE_URL", "\"http://YOUR_IP:8000\"")
buildConfigField("String", "WS_BASE_URL", "\"ws://YOUR_IP:8000\"")

// For production (cloud):
buildConfigField("String", "API_BASE_URL", "\"https://your-app.onrender.com\"")
buildConfigField("String", "WS_BASE_URL", "\"wss://your-app.onrender.com\"")
```

### Step 5: Run Android App

**In Android Studio:**
1. Open `ScamShieldAndroid` folder
2. Click "Sync Project with Gradle Files"
3. Click Run ▶️
4. Select device/emulator

**From Command Line:**
```bash
cd ScamShieldAndroid
./gradlew installDebug
```

### Step 6: Test the System! 🎉

1. **Launch app** on Android device
2. **Grant permissions** (phone, microphone, notifications)
3. **Register account** with email/password
4. **Enter phone number** and tap "Start Protection"
5. **Answer Twilio call**
6. **Merge suspicious call** following on-screen instructions
7. **Watch real-time risk meter** update!

---

## 📁 Project Structure

```
scam-voice-detector/
├── backend_new/              # FastAPI Backend
│   ├── app/
│   │   ├── api/             # REST endpoints
│   │   ├── models/          # Database models
│   │   ├── services/        # Twilio, AI services
│   │   └── main.py          # Application entry
│   ├── alembic/             # Database migrations
│   ├── docker-compose.yml   # Local development
│   ├── Dockerfile           # Container config
│   ├── requirements.txt     # Python dependencies
│   ├── README.md            # Full backend docs
│   └── QUICKSTART.md        # Quick setup guide
│
└── ScamShieldAndroid/       # Android App
    ├── app/
    │   ├── src/main/java/com/scamshield/
    │   │   ├── data/        # Repository, API clients
    │   │   ├── domain/      # Business logic
    │   │   ├── presentation/# UI (Compose)
    │   │   ├── service/     # Background services
    │   │   └── MainActivity.kt
    │   ├── build.gradle.kts # Dependencies
    │   └── google-services.json # Firebase config
    ├── README.md            # Android docs
    └── RUNNING_THE_APP.md  # Detailed run guide
```

---

## 🔗 How Everything Connects

```
┌─────────────────┐
│  Android App    │
│  (Jetpack       │
│   Compose UI)   │
└────────┬────────┘
         │
         ├─── HTTP REST ────→ ┌──────────────────┐
         │                    │  FastAPI Backend │
         │                    │  (Protection API)│
         │                    └────────┬─────────┘
         │                             │
         ├─── WebSocket ──────→ ┌─────┴────────┐
         │    (Socket.IO)       │  Socket.IO    │
         │                      │  (Real-time)  │
         │                      └───────────────┘
         │                             │
         │                    ┌────────┴────────┐
         │                    │                 │
         │                    ├─ Twilio Voice   │
         │                    │  (Conference)   │
         │                    │                 │
         │                    ├─ Resemble AI    │
         │                    │  (Deepfake)     │
         │                    │                 │
         │                    ├─ Deepgram       │
         │                    │  (Speech-to-    │
         │                    │   Text)         │
         │                    │                 │
         │                    └─ PostgreSQL     │
         │                       (Database)     │
         │                                      │
         └──── Firebase FCM ───────────────────┘
              (Push Notifications)
```

---

## 📱 Call Flow Explained

1. **User taps "Start Protection"** in Android app
   ```
   App → Backend: POST /api/v1/protection/start
   ```

2. **Backend initiates Twilio call** to user's phone
   ```
   Backend → Twilio: Create outbound call
   Twilio → User: Phone rings
   ```

3. **User answers** Scam Shield call
   ```
   User: Answers phone
   Twilio → Backend: Call status webhook
   ```

4. **User merges suspicious caller**
   ```
   User: Taps "Add Call" → Dials scammer → "Merge"
   Twilio: Creates conference with 3 participants
   ```

5. **Real-time analysis begins**
   ```
   Twilio → Backend: Audio stream (Media Streams)
   Backend → Resemble AI: Deepfake detection
   Backend → Deepgram: Speech-to-text
   Backend: Calculate risk score
   Backend → WebSocket: Emit to Android app
   ```

6. **Android app shows results**
   ```
   WebSocket → App: Real-time updates
   App: Updates risk meter (0-100%)
   App: Shows live transcript
   App: Alert if risk > 70%
   ```

---

## 🧪 Testing Checklist

### Backend Tests

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Check API docs
open http://localhost:8000/docs
```

### Android App Tests

- ✅ App builds successfully
- ✅ Can register/login
- ✅ Permissions granted
- ✅ Can start protection
- ✅ Receives Twilio call
- ✅ WebSocket connects
- ✅ Risk meter updates
- ✅ Transcript displays
- ✅ Alerts work

---

## 🌐 Deployment Options

### Backend Deployment

**Render (Easiest)**
```bash
# 1. Push code to GitHub
# 2. Create new Web Service on Render
# 3. Connect repo, add environment variables
# 4. Deploy!
```

**Railway**
```bash
railway init
railway add -d postgres
railway add -d redis
railway up
```

**Heroku**
```bash
heroku create
heroku addons:create heroku-postgresql
heroku addons:create heroku-redis
git push heroku main
```

See `backend_new/README.md` for detailed deployment guides.

### Android App Distribution

**Debug APK** (for testing)
```bash
cd ScamShieldAndroid
./gradlew assembleDebug
# APK at: app/build/outputs/apk/debug/app-debug.apk
```

**Google Play Store**
```bash
./gradlew bundleRelease
# Upload app/build/outputs/bundle/release/app-release.aab
```

---

## 🔒 Security Checklist

### Backend
- ✅ JWT token authentication
- ✅ Password hashing (bcrypt)
- ✅ HTTPS enforced
- ✅ CORS configured
- ✅ Environment variables for secrets
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Rate limiting (consider adding)

### Android
- ✅ Secure token storage (DataStore)
- ✅ HTTPS only (cleartext disabled)
- ✅ ProGuard obfuscation
- ✅ Permission validation
- ✅ Network security config

---

## 💰 Cost Estimation

### Development/Testing
- Twilio: $15 free credit → ~30-50 test calls
- Resemble AI: Free tier available
- Deepgram: Free tier available
- Firebase: Free tier (adequate for testing)
- **Total: ~$0** for initial testing

### Production (per month)
- Twilio phone number: $1/month
- Twilio calls: $0.013/min × usage
- Resemble API: Pay per use
- Deepgram: Pay per minute
- Hosting (Render/Railway): $7-25/month
- **Estimated: $10-50/month** for light usage

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Docker
docker-compose ps
docker-compose logs api

# Check database
docker-compose exec db psql -U postgres -d scamshield

# Restart everything
docker-compose down
docker-compose up -d
```

### Android App Won't Build
```bash
# Clean build
./gradlew clean

# Invalidate caches (Android Studio)
File → Invalidate Caches → Invalidate and Restart
```

### Twilio Not Calling
1. Check phone number format (+1...)
2. Verify Twilio credentials in `.env`
3. Check Twilio balance/trial status
4. View logs: https://console.twilio.com/monitor/logs

### WebSocket Not Connecting
1. Check CORS settings in backend `.env`
2. Verify WS URL format (ws:// or wss://)
3. Check firewall/network settings
4. Test WebSocket: https://www.websocket.org/echo.html

---

## 📚 Documentation

- **Backend**: `backend_new/README.md`
- **Backend Quick Start**: `backend_new/QUICKSTART.md`
- **Android**: `ScamShieldAndroid/README.md`
- **Running Android**: `ScamShieldAndroid/RUNNING_THE_APP.md`
- **Project Summary**: `ScamShieldAndroid/PROJECT_SUMMARY.md`

---

## 🎓 Learning Resources

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [Twilio Voice](https://www.twilio.com/docs/voice)
- [Socket.IO](https://socket.io/docs/v4/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)

---

## 🆘 Need Help?

1. **Backend issues**: Check `backend_new/README.md` troubleshooting section
2. **Android issues**: Check `ScamShieldAndroid/RUNNING_THE_APP.md`
3. **API keys**: Review `.env.example` for required format
4. **Twilio setup**: Check `backend_new/QUICKSTART.md` for step-by-step guide

---

## ✅ Quick Deployment Checklist

### Before Going Live:

- [ ] Get all API keys (Twilio, Resemble, Deepgram)
- [ ] Setup Firebase project
- [ ] Deploy backend to cloud (Render/Railway/Heroku)
- [ ] Configure environment variables
- [ ] Run database migrations
- [ ] Test backend API endpoints
- [ ] Update Android app with production URLs
- [ ] Test on physical Android device
- [ ] Enable HTTPS/SSL
- [ ] Set proper CORS origins
- [ ] Test end-to-end call flow
- [ ] Setup monitoring/logging
- [ ] Create backup strategy

---

## 🎉 Success!

You now have a complete, production-ready voice scam detection system!

**Next Steps:**
1. ✅ Get API keys
2. ✅ Start backend
3. ✅ Run Android app
4. ✅ Make test call
5. ✅ Deploy to production
6. ✅ Protect people from scams!

**Built with:**
- Kotlin + Jetpack Compose
- FastAPI + Python
- Twilio + AI Services
- PostgreSQL + Redis
- Docker + Cloud deployment

---

**Happy protecting! 🛡️**
