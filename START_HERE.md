# 🚀 How to Start This Project

This project has **two main components**:

1. **AI Influencer Platform** (Web App) - Main platform with browser interface
2. **Hunter.io Data Extractor** - Tool to extract influencer data from Hunter.io API

---

## 🎯 Quick Start: AI Influencer Platform (Recommended)

This is the main web application with a browser interface.

### Step 1: Install Dependencies

```bash
cd platform
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the `platform` directory:

```bash
cd platform
```

Create `.env` file with at minimum:

```env
# Required: OpenAI API Key (for GPT analysis)
OPENAI_API_KEY=your_openai_key_here

# Optional: Social Media APIs (platform works without these)
TWITTER_BEARER_TOKEN=your_token_here
INSTAGRAM_ACCESS_TOKEN=your_token_here
FACEBOOK_ACCESS_TOKEN=your_token_here
LINKEDIN_ACCESS_TOKEN=your_token_here

# Optional: Google Sheets Integration
GOOGLE_CREDENTIALS_FILE=../credentials.json
GOOGLE_SHEET_NAME=Influencer Data

# Server Configuration
PORT=5001
FLASK_DEBUG=False
```

**Minimum Required**: Just `OPENAI_API_KEY` - the platform will work with ChatGPT API alone!

### Step 3: Start the Server

```bash
cd platform
python simple_server.py
```

Or on Windows PowerShell:
```powershell
cd platform
python simple_server.py
```

The server will start on: **http://localhost:5001**

### Step 4: Open the Frontend

**Option A: Direct File** (Easiest)
- Navigate to `platform/frontend/index.html` and open it in your browser

**Option B: Local Server**
```bash
cd platform/frontend
python -m http.server 8000
# Then visit: http://localhost:8000/index.html
```

**Option C: Via Flask** (if configured)
- Visit: http://localhost:5001

---

## 📊 Alternative: Hunter.io Data Extractor

If you want to extract influencer data from Hunter.io API:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get Hunter.io API Key

1. Sign up at [hunter.io](https://hunter.io)
2. Go to Account Settings → API section
3. Copy your API key

### Step 3: Run Extractor

```bash
# Set API key as environment variable
export HUNTER_API_KEY=your_api_key_here

# Or pass via command line
python hunter_extractor.py --api-key YOUR_API_KEY --domains "techcrunch.com,forbes.com" --format csv
```

See `README.md` for more examples.

---

## ✅ Quick Checklist

### For AI Influencer Platform:
- [ ] Install dependencies: `cd platform && pip install -r requirements.txt`
- [ ] Create `.env` file with at least `OPENAI_API_KEY`
- [ ] Start server: `python simple_server.py`
- [ ] Open `platform/frontend/index.html` in browser
- [ ] Test by setting filters and clicking "Get AI Recommendations"

### For Hunter.io Extractor:
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Get Hunter.io API key
- [ ] Run: `python hunter_extractor.py --api-key YOUR_KEY --domains "example.com"`

---

## 🆘 Troubleshooting

### Server won't start?
- Check if port 5001 is already in use
- Make sure all dependencies are installed
- Check `.env` file exists and has `OPENAI_API_KEY`

### No influencers found?
- Make sure `OPENAI_API_KEY` is set correctly
- Try removing some filters
- Check server logs for error messages

### Frontend not loading?
- Make sure server is running on port 5001
- Check browser console for errors
- Try opening `index.html` directly as a file

---

## 📚 More Documentation

- **Platform Guide**: `platform/README.md`
- **API Setup**: `platform/QUICK_START_APIS.md`
- **Hunter.io Guide**: `README.md` (root)
- **Google Sheets Setup**: `GOOGLE_SHEETS_SETUP.md`

---

## 🎯 Recommended First Steps

1. **Start with the AI Influencer Platform** (it's the main feature)
2. **Get OpenAI API Key** (required for GPT analysis)
3. **Optional**: Add social media API keys for real data (see `platform/QUICK_START_APIS.md`)
4. **Test the platform** by searching for influencers

The platform works great with just the OpenAI API key - you can add social media APIs later!

