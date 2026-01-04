# 🤖 AI-Powered Influencer Recommendation Platform

An intelligent platform that uses AI/LLM to analyze influencers and recommend the best matches based on client requirements. No hard coding - the model learns and adapts!

## 🎯 Features

- ✅ **AI-Powered Recommendations** - Uses LLM to analyze and match influencers
- ✅ **Smart Filtering** - Filter by industry, location, engagement, content type
- ✅ **Content Analysis** - Analyzes influencer posts, views, and engagement
- ✅ **No Hard Coding** - Model-based recommendations, not rule-based
- ✅ **Real-time Analysis** - Get recommendations instantly
- ✅ **Beautiful Web Interface** - Easy-to-use client dashboard

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd platform
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Platform

```bash
python app.py
```

The API will run on `http://localhost:5000`

### 4. Open Web Interface

Open `frontend/index.html` in your browser, or serve it:

```bash
cd frontend
python -m http.server 8000
```

Then visit: `http://localhost:8000`

## 📊 How It Works

1. **Data Source**: Reads influencer data from Google Sheets
2. **Client Filters**: Client sets requirements (industry, location, etc.)
3. **AI Analysis**: LLM analyzes each influencer's:
   - Job title and expertise
   - Social media presence
   - Content type and engagement
   - Audience alignment
   - Overall fit with requirements
4. **Recommendations**: Returns ranked list with:
   - Match score (0-100)
   - AI reasoning
   - Key strengths
   - Potential concerns

## 🔧 API Endpoints

### Get Recommendations
```bash
POST /api/recommendations
{
  "filters": {
    "industry": "tech",
    "location": "United States",
    "min_followers": 10000,
    "content_type": ["tech reviews", "tutorials"],
    "target_audience": "tech enthusiasts"
  },
  "limit": 10
}
```

### Get All Influencers
```bash
GET /api/influencers
```

### Analyze Influencer
```bash
POST /api/analyze
{
  "influencer_id": "123"
}
```

## 🎨 Client Interface

The web interface allows clients to:
- Set filters and requirements
- Get AI-powered recommendations
- View match scores and reasoning
- See influencer details and social profiles

## 🤖 AI Model

- Uses OpenAI GPT-4 or GPT-4o-mini
- Analyzes influencer profiles intelligently
- Provides reasoning for recommendations
- Adapts to different client requirements

## 📈 Future Enhancements

- [ ] Real-time content analysis from social media
- [ ] Engagement rate calculations
- [ ] Historical performance tracking
- [ ] Campaign success prediction
- [ ] Multi-criteria optimization

## 🔐 Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required for AI features)
- `GOOGLE_CREDENTIALS_FILE` - Path to Google credentials JSON
- `GOOGLE_SHEET_NAME` - Name of your Google Sheet
- `PORT` - Server port (default: 5000)

## 💡 Usage Example

1. Client sets filters: "Tech industry, US-based, 10K+ followers"
2. Platform analyzes all influencers using AI
3. Returns top 10 matches with scores and reasoning
4. Client reviews recommendations and selects influencers

## 🎯 Benefits

- **No Hard Coding** - AI adapts to any requirement
- **Intelligent Matching** - Understands context and nuance
- **Scalable** - Works with any number of influencers
- **Explainable** - Provides reasoning for each recommendation

