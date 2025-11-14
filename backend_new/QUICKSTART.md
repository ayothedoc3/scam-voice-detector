# 🚀 Quick Start Guide

Get the Scam Shield backend running in 5 minutes!

## ⚡ Fastest Way (Docker)

```bash
# 1. Get API keys first (see below)

# 2. Navigate to backend
cd backend_new

# 3. Setup environment
cp .env.example .env

# 4. Edit .env and paste your API keys
nano .env  # or use any text editor

# 5. Start everything!
docker-compose up -d

# 6. Initialize database
docker-compose exec api alembic upgrade head

# 7. Done! Test it:
curl http://localhost:8000/health
```

**✅ API is now running at http://localhost:8000**

## 🔑 Get Your API Keys

### 1. Twilio (Required)

1. Sign up: https://www.twilio.com/try-twilio
2. Get **Account SID** and **Auth Token** from dashboard
3. Buy a phone number (Phone Numbers → Buy a Number)
   - Select one with **Voice** capability
   - Cost: ~$1/month

**Add to .env:**
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### 2. Resemble AI (Required)

1. Sign up: https://app.resemble.ai
2. Go to Settings → API Keys
3. Create new API key

**Add to .env:**
```
RESEMBLE_API_KEY=your_resemble_api_key
```

### 3. Deepgram (Required)

1. Sign up: https://console.deepgram.com
2. Create new API key
3. Copy the key

**Add to .env:**
```
DEEPGRAM_API_KEY=your_deepgram_api_key
```

### 4. Generate JWT Secret

```bash
# Run this command:
openssl rand -hex 32

# Copy the output and add to .env:
SECRET_KEY=paste_the_generated_key_here
```

## 📱 Connect Android App

Once backend is running:

1. **Get your backend URL**:
   - Local: `http://YOUR_IP:8000` (find with `ifconfig` or `ipconfig`)
   - Deploy to cloud for production

2. **Update Android app** (`app/build.gradle.kts`):
   ```kotlin
   buildConfigField("String", "API_BASE_URL", "\"http://YOUR_IP:8000\"")
   buildConfigField("String", "WS_BASE_URL", "\"ws://YOUR_IP:8000\"")
   ```

3. **Test connection**:
   ```bash
   # From Android device/emulator, test:
   curl http://YOUR_IP:8000/health
   ```

## 🧪 Test the API

### 1. Register a user

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "phone_number": "+1234567890"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from the response!

### 3. Start Protection

```bash
curl -X POST http://localhost:8000/api/v1/protection/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "user_phone": "+1234567890"
  }'
```

You should receive a call from Twilio!

## 📖 View API Documentation

Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Common Issues

### Port 8000 already in use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
docker-compose down
# Edit docker-compose.yml, change 8000:8000 to 8080:8000
docker-compose up -d
```

### Database connection error

```bash
# Restart PostgreSQL
docker-compose restart db

# Check logs
docker-compose logs db
```

### Twilio not calling

1. **Check phone number format**: Must include country code (+1...)
2. **Verify Twilio credentials** in .env
3. **Check Twilio account balance**
4. **View Twilio logs**: https://console.twilio.com/monitor/logs/calls

### WebSocket not connecting

1. **Check CORS settings** in .env
2. **Use correct URL format**: `ws://` or `wss://`
3. **Check firewall/network** settings

## 📊 Monitor Logs

```bash
# View all logs
docker-compose logs -f

# View API logs only
docker-compose logs -f api

# View database logs
docker-compose logs -f db
```

## 🛑 Stop Services

```bash
# Stop but keep data
docker-compose stop

# Stop and remove containers (keeps data)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

## 🔄 Update Code

```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose up -d --build

# Run new migrations
docker-compose exec api alembic upgrade head
```

## 🌐 Deploy to Production

See main README.md for deployment options:
- Render (easiest)
- Railway
- Heroku
- AWS/GCP/Azure

For production, you'll also need:
- Public HTTPS URL
- SSL certificate
- Domain name (optional)

## 💡 Pro Tips

1. **Use ngrok for local testing** with Twilio:
   ```bash
   ngrok http 8000
   # Use the https URL in Twilio webhooks
   ```

2. **Check database**:
   ```bash
   docker-compose exec db psql -U postgres -d scamshield
   ```

3. **Reset everything**:
   ```bash
   docker-compose down -v
   docker-compose up -d
   docker-compose exec api alembic upgrade head
   ```

## 🎉 Next Steps

1. ✅ Backend running
2. ✅ API keys configured
3. ✅ Test with curl/Postman
4. ✅ Connect Android app
5. ✅ Make a test call!

**Need help?** Check the full README.md for detailed documentation.

---

**Happy protecting! 🛡️**
