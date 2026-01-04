# 🚀 Quick Start - Easiest & Most Efficient Method

## ✅ **Domain Search is the BEST option** because:

1. **Most Efficient**: One API call = up to 100 contacts
2. **Easiest**: Just provide domain names (no need for email lists)
3. **Fastest**: Gets multiple results at once
4. **Perfect for Influencers**: Find all contacts in companies/domains

## 📋 Simple 3-Step Process:

### Step 1: Get your Hunter.io API Key
- Go to [hunter.io](https://hunter.io) → Account Settings → API
- Copy your API key

### Step 2: Choose domains to search
Examples:
- `techcrunch.com` - Tech journalists
- `forbes.com` - Business influencers  
- `mashable.com` - Digital media
- `theverge.com` - Tech influencers
- Or any company/website domain

### Step 3: Run this ONE command:

```bash
python3 hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains "techcrunch.com,forbes.com,mashable.com" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --limit 50
```

**That's it!** The script will:
- ✅ Search each domain
- ✅ Extract all contact data
- ✅ Export directly to your Google Sheet
- ✅ Format everything nicely

## 💡 Pro Tips:

- **Multiple domains**: Separate with commas: `"domain1.com,domain2.com,domain3.com"`
- **Limit results**: Use `--limit 50` to get 50 contacts per domain (max 100)
- **Check your sheet**: Refresh your Google Sheet to see results appear in real-time

## ⚡ Why Domain Search > Email Enrichment:

| Method | API Calls | Speed | Best For |
|--------|-----------|-------|----------|
| **Domain Search** | 1 call = 100 results | ⚡⚡⚡ Fast | Finding new influencers |
| Email Enrichment | 1 call = 1 result | 🐌 Slow | You already have emails |

**Domain Search is 100x more efficient!** 🎯


