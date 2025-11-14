# 🚀 Running the Scam Shield Android App

## ⚠️ Important: Environment Requirements

This is a **native Android application** that requires specific tools to run. It cannot run in a standard Linux terminal environment.

## 📋 Prerequisites

You need **ONE** of the following setups:

### Option 1: Android Studio (Recommended)
- Android Studio Hedgehog (2023.1.1) or later
- JDK 17
- Android SDK 34
- At least 8GB RAM
- 10GB free disk space

### Option 2: Command Line with Android SDK
- Android SDK Command-line Tools
- JDK 17
- Android device with USB debugging enabled OR Android Emulator

---

## 🎯 Method 1: Using Android Studio (Easiest)

### Step 1: Install Android Studio

**Download from**: https://developer.android.com/studio

**Install for your OS:**
- **Windows**: Run the `.exe` installer
- **macOS**: Drag to Applications folder
- **Linux**: Extract and run `studio.sh`

### Step 2: Configure Android Studio

1. **Open Android Studio**
2. **SDK Manager** (Tools → SDK Manager)
   - Check: Android SDK Platform 34
   - Check: Android SDK Build-Tools 34
   - Check: Android Emulator
   - Click "Apply" to download

### Step 3: Open the Project

```bash
# 1. Copy the ScamShieldAndroid folder to your local machine

# 2. Open Android Studio

# 3. Click "Open" and select the ScamShieldAndroid folder
```

### Step 4: Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Add Android app with package name: `com.scamshield`
4. Download `google-services.json`
5. Replace `ScamShieldAndroid/app/google-services.json` with your file

### Step 5: Configure API URLs

Edit `app/build.gradle.kts` and update:

```kotlin
buildConfigField("String", "API_BASE_URL", "\"https://your-backend-api.com\"")
buildConfigField("String", "WS_BASE_URL", "\"wss://your-backend-api.com\"")
```

### Step 6: Sync Project

1. Click **"Sync Project with Gradle Files"** (top toolbar)
2. Wait for sync to complete (first time takes 5-10 minutes)

### Step 7: Create Virtual Device (Optional)

If you don't have a physical device:

1. Tools → Device Manager
2. Click "Create Device"
3. Select "Pixel 6" or newer
4. Download System Image: Android 14.0 (API 34)
5. Click "Finish"

### Step 8: Run the App

**Option A: Physical Device**
```bash
1. Enable USB Debugging on your Android phone:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

2. Connect phone via USB

3. Click the green "Run" button ▶️ in Android Studio

4. Select your device from the list
```

**Option B: Emulator**
```bash
1. Click the green "Run" button ▶️

2. Select your virtual device

3. Wait for emulator to start (2-3 minutes first time)

4. App will install automatically
```

---

## 🎯 Method 2: Command Line Build

### Step 1: Install Android SDK

**Linux/macOS:**
```bash
# Download Android command-line tools
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip

# Extract
unzip commandlinetools-linux-11076708_latest.zip -d ~/android-sdk

# Set environment variables
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Install required packages
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
```

### Step 2: Build the App

```bash
cd ScamShieldAndroid

# Make gradlew executable
chmod +x gradlew

# Build debug APK
./gradlew assembleDebug

# Output: app/build/outputs/apk/debug/app-debug.apk
```

### Step 3: Install on Device

```bash
# Connect Android device with USB debugging enabled

# Install APK
adb install app/build/outputs/apk/debug/app-debug.apk

# Or if multiple devices:
adb -s <device-id> install app/build/outputs/apk/debug/app-debug.apk
```

---

## 📱 Testing on Physical Device

### Enable Developer Mode

1. **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Go back → **Developer Options**
4. Enable **USB Debugging**

### Connect via USB

```bash
# Check if device is connected
adb devices

# Should show:
List of devices attached
ABC123DEF456    device

# Install app
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

### Connect via WiFi (Optional)

```bash
# On device connected via USB:
adb tcpip 5555

# Find device IP (Settings → About → Status → IP address)
adb connect <device-ip>:5555

# Now you can disconnect USB
```

---

## 🐛 Troubleshooting

### "SDK not found"
```bash
# Set ANDROID_HOME environment variable
export ANDROID_HOME=/path/to/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### "Gradle sync failed"
```bash
# In Android Studio:
File → Invalidate Caches → Invalidate and Restart

# Or command line:
./gradlew clean
rm -rf .gradle
./gradlew build
```

### "Device not detected"
```bash
# Check USB debugging is enabled
adb devices

# If "unauthorized", check phone screen for authorization prompt

# If still not working:
adb kill-server
adb start-server
adb devices
```

### Build errors
```bash
# Clean build
./gradlew clean

# Rebuild
./gradlew assembleDebug --stacktrace
```

---

## ⚙️ Configuration Checklist

Before running, make sure you've configured:

- [ ] **Firebase**: Valid `google-services.json` file
- [ ] **API URLs**: Updated in `app/build.gradle.kts`
- [ ] **Permissions**: Grant all requested permissions when app launches
- [ ] **Backend**: Ensure your backend API is running and accessible

---

## 🎮 First Run Experience

When you first launch the app:

1. **Permission Requests**:
   - Phone state access ✓
   - Microphone access ✓
   - Call logs access ✓
   - Notifications ✓
   - Click "Allow" for all

2. **Main Screen**:
   - You'll see the Protection Screen
   - Enter a phone number
   - Click "Start Protection"

3. **Testing Without Backend**:
   - The app will attempt to connect to the API
   - If backend is not running, you'll see connection errors
   - This is expected - the UI will still render correctly

---

## 🔧 Development Commands

### Build Variants

```bash
# Debug build (for testing)
./gradlew assembleDebug

# Release build (for production)
./gradlew assembleRelease

# App Bundle (for Play Store)
./gradlew bundleRelease
```

### Running Tests

```bash
# Unit tests
./gradlew test

# Instrumented tests (requires device/emulator)
./gradlew connectedAndroidTest
```

### Generate APK

```bash
./gradlew assembleDebug

# APK location:
# app/build/outputs/apk/debug/app-debug.apk
```

---

## 📦 Distribution

### Debug APK (for testing)
```bash
./gradlew assembleDebug
# Share: app/build/outputs/apk/debug/app-debug.apk
```

### Release APK (signed)
1. Create keystore
2. Configure signing in `app/build.gradle.kts`
3. Build release: `./gradlew assembleRelease`

### Google Play Store
```bash
./gradlew bundleRelease
# Upload: app/build/outputs/bundle/release/app-release.aab
```

---

## 🌐 Backend Requirements

The app expects these endpoints:

### REST API
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `POST /api/v1/protection/start`
- `POST /api/v1/protection/stop`
- `GET /api/v1/protection/status/{callSid}`

### WebSocket
- `wss://your-api.com/socket.io/`
- Events: `join_call`, `analysis_update`

Make sure your backend is running before testing the app!

---

## 📱 Minimum Device Requirements

- **Android Version**: 8.0 (API 26) or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 100MB free space
- **Permissions**: Phone, Microphone, Notifications

---

## 🆘 Need Help?

- **Android Studio Guide**: https://developer.android.com/studio/intro
- **Gradle Guide**: https://developer.android.com/studio/build
- **ADB Guide**: https://developer.android.com/tools/adb

---

## ✅ Quick Start Summary

**Fastest way to run:**

1. Install Android Studio
2. Open the `ScamShieldAndroid` project
3. Replace `google-services.json` with your Firebase config
4. Update API URLs in `app/build.gradle.kts`
5. Click "Run" ▶️
6. Select device or emulator
7. Grant permissions when app launches

**That's it! The app should now be running.**

---

**Note**: This app requires an actual Android environment to run. You cannot run it in a standard terminal or web browser. It's specifically built for Android devices.
