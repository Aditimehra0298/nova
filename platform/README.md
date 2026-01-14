# 🚀 AI Influencer Platform

Complete influencer analysis platform with GPT-powered recommendations, real-time social media data, and comprehensive analytics.

## ✨ Features

- **Multi-Platform Discovery**: Find influencers from Instagram, Twitter, LinkedIn, Facebook
- **GPT-Powered Analysis**: AI analysis of profiles, hashtags, and engagement
- **Real API Integration**: Get actual views, hashtags, and engagement from social media APIs
- **Smart Ranking**: Recommendations based on real view counts and engagement
- **Profile Analysis**: Deep insights into influencer content, audience, and collaboration potential

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd platform
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_key
TWITTER_BEARER_TOKEN=your_twitter_token
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
FACEBOOK_ACCESS_TOKEN=your_facebook_token
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
GOOGLE_CREDENTIALS_FILE=../credentials.json
GOOGLE_SHEET_NAME=Influencer Data
PORT=5001
```

### 3. Start Server
```bash
python3 simple_server.py
```

### 4. Open Frontend
Open `frontend/index.html` in your browser

## 📚 API Setup

See [QUICK_START_APIS.md](QUICK_START_APIS.md) for easy API setup (5 minutes).

## 📡 API Endpoints

- `GET /api/health` - Health check
- `POST /api/recommendations` - Get AI recommendations
- `GET /api/analyze-profile/<id>` - Analyze influencer profile with GPT

## 🎯 Usage

1. Get recommendations using filters
2. Click "Analyze with GPT" on any influencer
3. See detailed analysis with real hashtags and views

## 📁 Project Structure

- `simple_server.py` - Main Flask server
- `data_manager.py` - Google Sheets integration
- `profile_analyzer.py` - GPT profile analysis
- `social_media_apis.py` - Social media API integrations
- `frontend/index.html` - Web interface


