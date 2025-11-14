# Scam Shield Android App

Production-ready native Android app for real-time voice scam detection using AI-powered deepfake analysis.

## 🚀 Features

- **Real-Time Voice Analysis**: Detects AI-generated voices during phone calls
- **Live Risk Monitoring**: Animated risk meter showing confidence levels
- **Twilio Integration**: Conference bridge routing for call analysis
- **WebSocket Updates**: Real-time analysis results via Socket.IO
- **Push Notifications**: Immediate alerts for high-risk calls
- **Call History**: Track and review past analyzed calls
- **Material Design 3**: Modern, beautiful UI with Jetpack Compose

## 📋 Prerequisites

- Android Studio Hedgehog | 2023.1.1 or later
- JDK 17
- Android SDK 34
- Minimum Android 8.0 (API 26)
- Firebase account (for push notifications)

## 🛠️ Technology Stack

- **Language**: Kotlin
- **UI**: Jetpack Compose + Material Design 3
- **Architecture**: MVVM + Clean Architecture
- **DI**: Hilt/Dagger
- **Database**: Room
- **Networking**: Retrofit + OkHttp
- **WebSocket**: OkHttp WebSocket
- **Async**: Coroutines + Flow
- **Push Notifications**: Firebase Cloud Messaging

## 📦 Project Structure

```
app/
├── data/                  # Data layer
│   ├── local/            # Room database
│   ├── remote/           # API & WebSocket clients
│   └── repository/       # Repository implementations
├── domain/               # Business logic layer
│   ├── model/           # Domain models
│   ├── repository/      # Repository interfaces
│   └── usecase/         # Use cases
├── presentation/        # UI layer
│   ├── components/      # Reusable UI components
│   ├── navigation/      # Navigation graph
│   ├── protection/      # Main feature screens
│   └── theme/           # App theme
├── service/             # Background services
├── receiver/            # Broadcast receivers
└── util/                # Utilities
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd scam-voice-detector/ScamShieldAndroid
```

### 2. Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing
3. Add an Android app with package name: `com.scamshield`
4. Download `google-services.json`
5. Place it in `app/` directory

### 3. Configure API Endpoints

Edit `app/build.gradle.kts`:

```kotlin
buildConfigField("String", "API_BASE_URL", "\"https://your-api-url.com\"")
buildConfigField("String", "WS_BASE_URL", "\"wss://your-api-url.com\"")
```

### 4. Sync and Build

```bash
./gradlew build
```

## 🏃 Running the App

### From Android Studio

1. Open project in Android Studio
2. Wait for Gradle sync
3. Select device/emulator
4. Click Run ▶️

### From Command Line

```bash
# Debug build
./gradlew installDebug

# Release build (requires signing config)
./gradlew assembleRelease
```

## 📱 App Permissions

The app requires these permissions:

- `READ_PHONE_STATE` - Detect incoming/outgoing calls
- `CALL_PHONE` - Initiate call to protection bridge
- `READ_CALL_LOG` - Access call history
- `RECORD_AUDIO` - Capture audio for analysis
- `POST_NOTIFICATIONS` - Show scam alerts
- `INTERNET` - API communication
- `FOREGROUND_SERVICE` - Background protection

## 🔐 Security

- HTTPS-only communication (cleartext disabled)
- Secure token storage with DataStore
- ProGuard/R8 code obfuscation
- Network security config
- No sensitive data in logs (production)

## 🧪 Testing

```bash
# Run unit tests
./gradlew test

# Run instrumented tests
./gradlew connectedAndroidTest
```

## 📦 Building for Production

### 1. Configure Signing

Create `keystore.properties`:

```properties
storePassword=<password>
keyPassword=<password>
keyAlias=<alias>
storeFile=<path-to-keystore>
```

### 2. Build Release APK

```bash
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

### 3. Build App Bundle (for Play Store)

```bash
./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

## 🔧 Configuration

### API URLs

Edit in `app/build.gradle.kts`:

```kotlin
buildConfigField("String", "API_BASE_URL", "\"https://api.scamshield.app\"")
buildConfigField("String", "WS_BASE_URL", "\"wss://api.scamshield.app\"")
```

### Database

Database name: `scam_shield_db`
Version: 1
Location: `data/local/ScamShieldDatabase.kt`

### Notification Channels

- **Protection**: Active call monitoring
- **Alerts**: High-risk scam warnings
- **General**: App notifications

## 📝 Key Components

### ProtectionScreen

Main feature screen with three states:
1. **Start Protection**: Phone number input
2. **Call Merging**: Instructions to merge calls
3. **Active Protection**: Real-time monitoring with risk meter

### RiskMeter

Animated circular progress indicator showing risk level (0-100%).

### WebSocket Client

Connects to backend for real-time analysis updates via Socket.IO.

### Protection Service

Foreground service managing active call protection with persistent notification.

## 🐛 Troubleshooting

### Build Fails

```bash
# Clean build
./gradlew clean

# Invalidate caches (Android Studio)
File > Invalidate Caches > Invalidate and Restart
```

### WebSocket Not Connecting

- Check `WS_BASE_URL` in build config
- Verify network permissions
- Check backend is running
- Review Logcat for errors

### Permissions Not Working

- Verify AndroidManifest.xml
- Check runtime permission requests
- Test on physical device (not emulator)

## 📚 Documentation

- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [Hilt Dependency Injection](https://dagger.dev/hilt/)
- [Room Database](https://developer.android.com/training/data-storage/room)
- [Retrofit](https://square.github.io/retrofit/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Email: support@scamshield.app

---

**Built with ❤️ using Kotlin and Jetpack Compose**
