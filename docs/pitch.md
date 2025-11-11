# Voice Scam Detector - Hackathon Pitch

## Problem
Phone scams using AI-generated voices are on the rise. Fraudsters can now clone voices to impersonate family members, CEOs, or trusted institutions, making scams more convincing and dangerous.

## Solution
Real-time deepfake voice detection tool that analyzes audio to identify AI-generated voices and protect users from sophisticated scam attempts.

## How It Works
1. User uploads suspicious audio (voicemail, recorded call, etc.)
2. Our backend analyzes the audio using Resemble AI's detection API
3. Results show confidence score and highlights suspicious segments
4. User gets instant verdict: authentic or AI-generated

## Technology Stack
- **Backend**: FastAPI + Resemble AI API
- **Frontend**: Streamlit
- **Audio Processing**: pydub
- **Deployment**: Render/Railway + Streamlit Cloud

## Target Users
- Individuals receiving suspicious calls
- Financial institutions
- Customer service teams
- Elderly users vulnerable to scams

## Business Model (Future)
- Freemium: 5 free analyses/month
- Premium: Unlimited analyses + API access
- Enterprise: Bulk processing + custom integration

## Team
- **Ay**: API Integration & Coordination
- **Raimy**: Backend Infrastructure
- **Sam**: Frontend Development

## Built for Tesonet AI Hackathon 2025

---

## Demo Script
1. "Meet our Voice Scam Detector - protecting you from AI-powered phone scams"
2. Upload sample scam audio
3. Show real-time analysis
4. Reveal confidence score + explanation
5. Compare with authentic voice sample

## Why This Matters
With voice cloning technology becoming accessible, we need equally powerful detection tools to protect vulnerable populations from financial and emotional harm.
