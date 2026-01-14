# 🚀 Render Deployment Guide

This guide will help you deploy the NOVA Influencer Platform to Render.

## ✅ Pre-Deployment Checklist

### Files Created/Updated for Render:
- ✅ `Procfile` - Tells Render how to start the app
- ✅ `render.yaml` - Optional configuration file
- ✅ `platform/simple_server.py` - Updated to use environment-based debug mode
- ✅ `platform/frontend/index.html` - Updated API URL to work in production
- ✅ `platform/data_manager.py` - Made CSV path configurable via environment variable

## 📋 Deployment Steps

### Step 1: Push to GitHub/GitLab
Make sure your code is in a Git repository (GitHub, GitLab, or Bitbucket).

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Connect your Git repository

### Step 3: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Select the repository and branch

### Step 4: Configure Service Settings

**Basic Settings:**
- **Name**: `nova-influencer-platform` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
  - (The root requirements.txt now includes all Flask and platform dependencies)
- **Start Command**: `cd platform && python simple_server.py`
  
**Alternative Build Command** (if you prefer to use platform/requirements.txt):
- **Build Command**: `pip install -r platform/requirements.txt`

**OR** if you're using the `render.yaml` file:
- Render will automatically detect and use `render.yaml` settings

### Step 5: Set Environment Variables

In Render Dashboard → Your Service → Environment:

**Required:**
```
OPENAI_API_KEY=your_openai_api_key_here
PORT=10000
FLASK_DEBUG=false
```

**Optional (but recommended):**
```
HUNTER_API_KEY=your_hunter_api_key_here
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Influencer Data
CSV_FILE_PATH=../Indian_Influencers_Master_List.csv
```

**Social Media APIs (Optional):**
```
INSTAGRAM_ACCESS_TOKEN=your_token
TWITTER_BEARER_TOKEN=your_token
LINKEDIN_ACCESS_TOKEN=your_token
FACEBOOK_ACCESS_TOKEN=your_token
```

### Step 6: Add Files to Repository

Make sure these files are in your repository:
- ✅ `Indian_Influencers_Master_List.csv` (in root directory)
- ✅ `platform/` folder with all Python files
- ✅ `platform/frontend/index.html`
- ✅ `platform/requirements.txt`
- ✅ `Procfile` (in root)
- ✅ `.env` (should be in `.gitignore`, don't commit secrets!)

### Step 7: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Install dependencies from `platform/requirements.txt`
   - Start the server using the `Procfile`
   - Make it available at `https://your-service-name.onrender.com`

## 🔧 Important Notes

### Port Configuration
- Render automatically sets the `PORT` environment variable
- The app uses `PORT` (defaults to 5001 if not set)
- Render typically uses port `10000`

### CSV File Location
- The CSV file `Indian_Influencers_Master_List.csv` should be in the repository root
- The app looks for it at `../Indian_Influencers_Master_List.csv` relative to `platform/` folder
- You can override with `CSV_FILE_PATH` environment variable

### Google Sheets Credentials
- If using Google Sheets, you need to upload `credentials.json` to Render
- Option 1: Add as a Secret File in Render dashboard
- Option 2: Base64 encode and store as environment variable (not recommended)
- Option 3: Use environment variables for service account (advanced)

### Large Dependencies
The `platform/requirements.txt` includes:
- `torch` and `transformers` (large ML libraries)
- These will increase build time but are fine for deployment

If you want faster builds and don't need ML features, you can create a lighter `requirements.txt` without them.

### Debug Mode
- `FLASK_DEBUG=false` for production (set in environment variables)
- Debug mode is disabled by default in production for security

## 🧪 Testing After Deployment

1. **Health Check**: Visit `https://your-service.onrender.com/api/health`
   - Should return: `{"status": "healthy", "message": "AI Influencer Platform API", "version": "2.0"}`

2. **Frontend**: Visit `https://your-service.onrender.com/`
   - Should show the web interface

3. **API Test**: Test the recommendations endpoint
   ```bash
   curl -X POST https://your-service.onrender.com/api/recommendations \
     -H "Content-Type: application/json" \
     -d '{"filters": {}, "limit": 5}'
   ```

## 🐛 Troubleshooting

### Build Fails
- Check that `platform/requirements.txt` exists
- Verify Python version (Render supports 3.7+)
- Check build logs for specific errors

### App Crashes on Start
- Check that `PORT` environment variable is set
- Verify all required environment variables are set
- Check logs in Render dashboard

### CSV File Not Found
- Verify `Indian_Influencers_Master_List.csv` is in repository root
- Check file path in logs
- Set `CSV_FILE_PATH` environment variable if needed

### API Returns 404
- Verify frontend is using relative API URLs (already fixed)
- Check that routes are correct
- Verify CORS is enabled (already configured)

### Frontend Can't Connect to API
- The frontend now uses `window.location.origin + '/api'` which should work
- If issues persist, check browser console for errors

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | Yes | 5001 | Server port (Render sets this automatically) |
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for AI features |
| `FLASK_DEBUG` | No | false | Enable Flask debug mode |
| `HUNTER_API_KEY` | No | - | Hunter.io API key |
| `GOOGLE_CREDENTIALS_FILE` | No | credentials.json | Path to Google credentials |
| `GOOGLE_SHEET_NAME` | No | Influencer Data | Google Sheet name |
| `CSV_FILE_PATH` | No | ../Indian_Influencers_Master_List.csv | Path to CSV file |
| `INSTAGRAM_ACCESS_TOKEN` | No | - | Instagram API token |
| `TWITTER_BEARER_TOKEN` | No | - | Twitter API token |
| `LINKEDIN_ACCESS_TOKEN` | No | - | LinkedIn API token |
| `FACEBOOK_ACCESS_TOKEN` | No | - | Facebook API token |

## 🎉 Success!

Once deployed, your platform will be available at:
`https://your-service-name.onrender.com`

The app will automatically:
- Load influencer data from CSV
- Serve the frontend interface
- Handle API requests
- Use environment variables for configuration

## 💡 Pro Tips

1. **Free Tier Limits**: Render free tier spins down after 15 minutes of inactivity. Consider upgrading for always-on service.

2. **Custom Domain**: You can add a custom domain in Render dashboard → Settings → Custom Domain

3. **Auto-Deploy**: Render automatically deploys on every push to your main branch (if enabled)

4. **Logs**: Monitor logs in Render dashboard → Logs tab

5. **Environment Variables**: Keep sensitive keys in Render's environment variables, not in code

6. **Database**: If you need persistent storage, consider adding a PostgreSQL database in Render

---

**Ready to deploy?** Follow the steps above and your platform will be live in minutes! 🚀

