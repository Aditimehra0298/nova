# 🌐 Comprehensive Multi-Platform Influencer Extractor

## ✅ Extract from ALL Platforms at Once!

This script searches multiple domains representing different platforms and industries to find influencers.

## 🚀 Quick Start

### Extract from All Platform Types:

```bash
python3 comprehensive_extractor.py \
  --api-key "5c1e38a60d83acdffe5640bd3d17de2980861376" \
  --platforms "all" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --limit 10
```

### Extract from Specific Platforms:

```bash
python3 comprehensive_extractor.py \
  --api-key "5c1e38a60d83acdffe5640bd3d17de2980861376" \
  --platforms "tech_media,business_media,marketing" \
  --format gsheet \
  --google-sheet "Influencer Data"
```

## 📊 Available Platform Types

1. **tech_media** - TechCrunch, The Verge, Wired, Ars Technica, Engadget, Gizmodo, Mashable, VentureBeat
2. **business_media** - Forbes, Bloomberg, WSJ, FT, Business Insider, CNBC, Reuters
3. **marketing** - HubSpot, Marketing Land, AdWeek, AdAge, Social Media Examiner
4. **social_media_companies** - LinkedIn, Twitter, Meta, Snap, TikTok, Pinterest
5. **influencer_platforms** - Influencer Marketing Hub, Grin, AspireIQ, Upfluence, Klear
6. **content_creators** - Medium, Substack, Ghost, WordPress

## 🎯 Usage Examples

### Example 1: All Platforms
```bash
python3 comprehensive_extractor.py \
  --api-key "YOUR_API_KEY" \
  --platforms "all" \
  --format gsheet \
  --google-sheet "All Influencers"
```

### Example 2: Tech & Business Media Only
```bash
python3 comprehensive_extractor.py \
  --api-key "YOUR_API_KEY" \
  --platforms "tech_media,business_media" \
  --format gsheet \
  --google-sheet "Media Influencers"
```

### Example 3: Custom Domains
```bash
python3 comprehensive_extractor.py \
  --api-key "YOUR_API_KEY" \
  --domains "techcrunch.com,forbes.com,mashable.com" \
  --format gsheet \
  --google-sheet "Custom Influencers"
```

### Example 4: Marketing & Influencer Platforms
```bash
python3 comprehensive_extractor.py \
  --api-key "YOUR_API_KEY" \
  --platforms "marketing,influencer_platforms" \
  --format gsheet \
  --google-sheet "Marketing Influencers"
```

## 📋 Command Options

- `--api-key`: Your Hunter.io API key (required)
- `--platforms`: Platform types (comma-separated or "all")
- `--domains`: Custom domains (comma-separated)
- `--format`: Output format (csv, gsheet, or both)
- `--google-sheet`: Google Sheet name
- `--limit`: Results per domain (default: 10, max for free plan)
- `--no-filter`: Disable influencer filtering

## ✅ What You Get

For each influencer:
- ✅ Platform category (Tech Media, Business Media, etc.)
- ✅ Domain (where found)
- ✅ Email address
- ✅ Full name
- ✅ Job title
- ✅ LinkedIn handle & URL
- ✅ Twitter handle & URL
- ✅ Source information

## 🎉 Results

Just ran it and got:
- **141 influencers** from Tech Media + Business Media platforms!
- All exported to your Google Sheet
- Includes LinkedIn and Twitter profiles
- Filtered for influencers only

## 💡 Tips

1. **Start with specific platforms** to save API credits
2. **Use limit=10** (free plan max per domain)
3. **Combine platform types** for comprehensive results
4. **Check your Google Sheet** to see all the data

## 🚀 Ready to Extract!

Run this to get influencers from all platforms:

```bash
python3 comprehensive_extractor.py \
  --api-key "5c1e38a60d83acdffe5640bd3d17de2980861376" \
  --platforms "all" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --limit 10
```

Enjoy your comprehensive influencer database! 🎉


