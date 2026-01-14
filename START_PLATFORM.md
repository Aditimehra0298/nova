# 🚀 Start the Platform in Browser

## Quick Start

### Step 1: Start Backend Server

```bash
cd platform
python3 app.py
```

Server will run on: **http://localhost:5001**

### Step 2: Open Frontend

**Option A: Direct File**

- Open `platform/frontend/index.html` in your browser

**Option B: Local Server**

```bash
cd platform/frontend
python3 -m http.server 8000
# Then visit: http://localhost:8000/index.html
```

**Option C: From Project Root**

```bash
cd /Users/aditimehra/Documents/nova
python3 -m http.server 8000
# Then visit: http://localhost:8000/platform/frontend/index.html
```

## ✅ Everything is Ready!

- ✅ Backend API: http://localhost:5001
- ✅ Frontend: platform/frontend/index.html
- ✅ OpenAI API: Configured
- ✅ Google Sheets: Connected (88 influencers)

## 🎯 How to Use

1. **Start the backend server** (Terminal 1):

   ```bash
   cd platform
   python3 app.py
   ```

2. **Open the frontend** in your browser:

   - File: `platform/frontend/index.html`
   - Or serve it with a local server

3. **Set filters** and click "Get AI Recommendations"

4. **View results** with AI-powered match scores!

## 📊 Test It

```bash
cd platform
python3 test_recommendations.py
```

