# 🔧 Render Deployment Troubleshooting Guide

## Issue: No Results Showing on Render (But Works Locally)

### Quick Diagnosis

1. **Check System Status**:
   ```
   GET https://your-app.onrender.com/api/system-status
   ```
   
   This will show:
   - Is ChatGPT API configured?
   - Is OpenAI API key set?
   - Environment variables status

2. **Check Render Logs**:
   - Go to Render Dashboard → Your Service → Logs
   - Look for error messages starting with `❌` or `⚠️`
   - Check for "OPENAI_API_KEY not found" messages

---

## Common Issues & Solutions

### Issue 1: OPENAI_API_KEY Not Set

**Symptoms:**
- No results returned
- Error: "ChatGPT API is not configured"
- System status shows `chatgpt_available: false`

**Solution:**
1. Go to Render Dashboard → Your Service → Environment
2. Add environment variable:
   ```
   Key: OPENAI_API_KEY
   Value: sk-your-actual-api-key-here
   ```
3. Click "Save Changes"
4. Service will automatically redeploy

**Verify:**
- Visit `/api/system-status` endpoint
- Should show `"openai_key_configured": true`

---

### Issue 2: API Key Set But Still Not Working

**Symptoms:**
- System status shows key exists
- But `chatgpt_available: false`
- Errors in logs about API initialization

**Possible Causes:**

1. **Invalid API Key Format**
   - Check key starts with `sk-`
   - Check key is at least 20 characters
   - Verify key is active in OpenAI dashboard

2. **API Key Has Wrong Permissions**
   - Ensure key has access to GPT-4o-mini model
   - Check OpenAI account has credits/quota

3. **Environment Variable Not Loading**
   - Check variable name is exactly `OPENAI_API_KEY` (case-sensitive)
   - No extra spaces or quotes
   - Restart service after adding

**Solution:**
1. Double-check API key in Render dashboard
2. Test API key locally:
   ```bash
   export OPENAI_API_KEY=your-key
   python -c "import os; from openai import OpenAI; client = OpenAI(); print('OK')"
   ```
3. If local test fails, get new API key from OpenAI

---

### Issue 3: Timeout Issues

**Symptoms:**
- Request takes too long
- Frontend shows timeout error
- Logs show "Request timed out"

**Solution:**
1. Reduce `limit` parameter (try 5 instead of 10)
2. Remove some filters (especially product_type, content_type)
3. Check Render logs for slow API calls

---

### Issue 4: CORS or Frontend Connection Issues

**Symptoms:**
- Frontend can't connect to API
- Browser console shows CORS errors
- "Failed to fetch" errors

**Solution:**
1. Check frontend is using correct API URL:
   - Should use: `window.location.origin + '/api'`
   - NOT hardcoded localhost URLs
2. Verify CORS is enabled in `simple_server.py`:
   ```python
   CORS(app)  # Should be present
   ```

---

## Step-by-Step Debugging

### Step 1: Check Environment Variables

In Render Dashboard → Environment, verify:
- ✅ `OPENAI_API_KEY` is set (not empty, not placeholder)
- ✅ `PORT` is set (usually auto-set by Render)
- ✅ `FLASK_DEBUG` is set to `false` (production)

### Step 2: Check System Status Endpoint

Visit: `https://your-app.onrender.com/api/system-status`

Expected response:
```json
{
  "success": true,
  "chatgpt_available": true,
  "openai_key_configured": true,
  "openai_key_length": 51
}
```

If `chatgpt_available: false`, check the `diagnostics` field for details.

### Step 3: Check Render Logs

Look for these log messages:

**Good signs:**
- `✅ OpenAI API key found (length: XX chars)`
- `✅ ChatGPT initialized with LangChain`
- `✅ Found X influencers using ChatGPT API`

**Bad signs:**
- `❌ OPENAI_API_KEY not found!`
- `⚠️ Error initializing ChatGPT`
- `⚠️ ChatGPT returned no influencers`

### Step 4: Test API Endpoint Directly

```bash
curl -X POST https://your-app.onrender.com/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"filters": {"industry": "Technology"}, "limit": 5}'
```

Check response:
- If `success: false`, read the `error` field
- If `success: true` but `count: 0`, filters might be too restrictive

---

## Quick Fixes

### Fix 1: Re-add Environment Variable

1. Remove `OPENAI_API_KEY` from Render
2. Add it again (copy-paste fresh)
3. Save and wait for redeploy
4. Check `/api/system-status` again

### Fix 2: Restart Service

1. Render Dashboard → Your Service
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Wait for deployment to complete
4. Test again

### Fix 3: Check API Key Validity

Test your API key:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Should return list of models. If error, key is invalid.

---

## Environment Variable Checklist

Before deploying, ensure these are set in Render:

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `OPENAI_API_KEY` | ✅ Yes | `sk-...` | Must be valid OpenAI key |
| `PORT` | ✅ Auto | `10000` | Set automatically by Render |
| `FLASK_DEBUG` | ⚠️ Recommended | `false` | Should be false in production |

Optional:
| `TWITTER_BEARER_TOKEN` | No | `...` | For Twitter data |
| `INSTAGRAM_ACCESS_TOKEN` | No | `...` | For Instagram data |
| `LINKEDIN_ACCESS_TOKEN` | No | `...` | For LinkedIn data |

---

## Still Not Working?

### Check These:

1. **Render Logs** - Full error messages
2. **System Status Endpoint** - `/api/system-status`
3. **API Key Format** - Starts with `sk-`, 51+ characters
4. **OpenAI Account** - Has credits/quota available
5. **Model Access** - Account has access to `gpt-4o-mini`

### Get More Help:

1. Copy full error from Render logs
2. Check `/api/system-status` response
3. Test API key locally first
4. Verify all environment variables are set correctly

---

## Expected Behavior

**Working correctly:**
- `/api/system-status` shows `chatgpt_available: true`
- `/api/recommendations` returns influencers
- Frontend displays results

**Not working:**
- `/api/system-status` shows `chatgpt_available: false`
- `/api/recommendations` returns error
- Frontend shows "No results" or error message

---

## Pro Tips

1. **Always test `/api/system-status` first** - fastest way to diagnose
2. **Check Render logs immediately after deployment** - errors show up there
3. **Test API key locally** - if it works locally, it's an environment variable issue
4. **Use minimal filters** - too many filters can cause empty results even with valid API key

