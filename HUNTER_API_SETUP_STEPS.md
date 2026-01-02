# 🔑 Step-by-Step: Create/Get Hunter.io API Key

## 📋 Complete Guide:

### Step 1: Log In to Hunter.io
1. Go to: [https://hunter.io](https://hunter.io)
2. Click **"Log In"** (top right)
3. Enter your email and password
4. Click **"Log In"**

### Step 2: Navigate to API Settings

**Option A: Via Profile Menu**
1. After logging in, look at the **top right corner**
2. Click on your **profile icon** (your initials or photo)
3. A dropdown menu will appear
4. Click **"Account Settings"** or **"Settings"**

**Option B: Direct URL**
- Go directly to: [https://hunter.io/users/me](https://hunter.io/users/me)
- This takes you to your account settings

### Step 3: Find API Section
1. In the **left sidebar menu**, look for:
   - **"API"** or
   - **"API Key"** or
   - **"Developer"** or
   - **"Integrations"**
2. Click on it

### Step 4: View/Copy Your API Key
1. You'll see your **API Key** displayed
   - It looks like: `abc123def456ghi789jkl012mno345pqr678stu901vwx234yz`
   - It's a long string of letters and numbers
2. Click the **"Copy"** button next to it
   - Or select the entire key and copy it (Ctrl+C / Cmd+C)

### Step 5: Save Your API Key
- **Important**: Save it somewhere safe
- You'll need it to run the extraction script

## 🚀 After Getting Your API Key:

### Option 1: Set as Environment Variable
```bash
export HUNTER_API_KEY="your_api_key_here"
```

### Option 2: Use in Command
```bash
python3 hunter_extractor.py \
  --api-key "your_api_key_here" \
  --domains "techcrunch.com,forbes.com" \
  --format gsheet \
  --google-sheet "Influencer Data"
```

## ⚠️ If You Don't See API Section:

1. **Check your plan**: 
   - Free plan: 25 searches/month (API access included)
   - Make sure you're on a plan that includes API access

2. **Look in different places**:
   - Try: Dashboard → Settings → API
   - Try: Account → API
   - Try: Integrations → API

3. **Contact Support**:
   - If you can't find it, contact Hunter.io support
   - They can help you locate your API key

## 📸 What to Look For:

- **API Key** section in settings
- A long string of characters (usually 40+ characters)
- A "Copy" or "Show" button
- Sometimes labeled as "API Token" or "Access Token"

## ✅ Once You Have It:

Share it with me (or set it as environment variable) and I'll help you run the extraction!


