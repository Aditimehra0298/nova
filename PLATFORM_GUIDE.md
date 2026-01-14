# 🤖 AI Influencer Recommendation Platform

## 🎯 What It Does

An intelligent platform that:
1. **Reads all influencer data** from your Google Sheet
2. **Client sets filters** (industry, location, engagement, content type, etc.)
3. **AI analyzes** each influencer's:
   - Job title and expertise
   - Social media presence and engagement
   - Content type and audience
   - Overall fit with client requirements
4. **Recommends best matches** with:
   - Match score (0-100%)
   - AI reasoning (why this influencer is a good match)
   - Key strengths
   - Potential concerns

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd platform
pip install -r requirements.txt
```

### Step 2: Set Up Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

### Step 3: Start the Platform

```bash
./start.sh
```

Or manually:
```bash
python app.py
```

### Step 4: Open Web Interface

Open `frontend/index.html` in your browser, or:

```bash
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

## 📊 How It Works

### Backend (API)
- **Flask API** on port 5000
- **Data Manager**: Reads from Google Sheets
- **Recommendation Engine**: Uses AI/LLM to analyze and recommend

### Frontend (Web Interface)
- **Client Dashboard**: Set filters and requirements
- **Results Display**: View AI recommendations with scores
- **Real-time**: Get recommendations instantly

### AI Model
- Uses **OpenAI GPT-4** or **GPT-4o-mini**
- **No hard coding** - AI understands context
- Analyzes influencer profiles intelligently
- Provides reasoning for each recommendation

## 🎨 Features

### For Clients:
- ✅ Set custom filters (industry, location, engagement, etc.)
- ✅ Get AI-powered recommendations
- ✅ See match scores and reasoning
- ✅ View influencer details and social profiles
- ✅ No technical knowledge needed

### For Platform:
- ✅ Reads from Google Sheets automatically
- ✅ AI analyzes all influencers
- ✅ Adapts to any client requirement
- ✅ No hard coding needed
- ✅ Scalable to any number of influencers

## 📋 API Usage

### Get Recommendations

```bash
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "industry": "tech",
      "location": "United States",
      "min_followers": 10000,
      "content_type": ["tech reviews"],
      "target_audience": "tech enthusiasts"
    },
    "limit": 10
  }'
```

### Get All Influencers

```bash
curl http://localhost:5000/api/influencers
```

## 🔧 Configuration

Edit `.env` file:
- `OPENAI_API_KEY` - Your OpenAI API key (required for AI)
- `GOOGLE_CREDENTIALS_FILE` - Path to credentials.json
- `GOOGLE_SHEET_NAME` - Your Google Sheet name
- `PORT` - Server port (default: 5000)

## 💡 Example Workflow

1. **Client opens web interface**
2. **Sets requirements**:
   - Industry: Tech
   - Location: United States
   - Min Followers: 10,000
   - Content Type: Tech reviews, tutorials
3. **Clicks "Get AI Recommendations"**
4. **AI analyzes** all influencers in your Google Sheet
5. **Returns top 10** with:
   - Match scores
   - Why each influencer is a good match
   - Key strengths
   - Social media profiles
6. **Client reviews** and selects influencers

## 🎯 Benefits

- **No Hard Coding**: AI adapts to any requirement
- **Intelligent**: Understands context and nuance
- **Explainable**: Provides reasoning for recommendations
- **Scalable**: Works with any number of influencers
- **User-Friendly**: Beautiful web interface

## 🔐 Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up / Log in
3. Go to API Keys section
4. Create new API key
5. Add to `.env` file

## ✅ Ready to Use!

The platform is ready. Just:
1. Add your OpenAI API key
2. Start the server
3. Open the web interface
4. Start getting AI recommendations!


