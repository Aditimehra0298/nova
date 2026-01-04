# 🎯 Influencer Filtering - Extract Only Influencers

## ✅ **Automatic Influencer Filtering is ENABLED by default!**

The script now automatically filters results to show **ONLY influencers** based on:

### 🔍 Filter Criteria:

1. **Job Titles** - Looks for keywords like:
   - Influencer, Content Creator, Blogger, Vlogger
   - Social Media Manager, Community Manager
   - Journalist, Reporter, Editor, Writer, Author
   - Podcaster, Host, Presenter
   - Marketing, PR, Brand Ambassador
   - And more...

2. **Social Media Presence** - Includes profiles with:
   - LinkedIn profile
   - Twitter/X handle
   - Instagram handle
   - YouTube channel
   - Facebook profile

3. **Job Roles** - Checks role field for influencer-related terms

## 🚀 Usage:

### Default (Influencers Only):
```bash
python3 hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains "techcrunch.com,forbes.com" \
  --format gsheet \
  --google-sheet "Influencer Data"
```
**This will ONLY extract influencers!** ✅

### To Get ALL Contacts (No Filtering):
```bash
python3 hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains "techcrunch.com" \
  --format gsheet \
  --google-sheet "All Contacts" \
  --no-filter
```

## 📊 What Gets Filtered:

**✅ INCLUDED (Influencers):**
- Content creators, bloggers, vloggers
- Social media managers
- Journalists, reporters, editors
- Marketing professionals
- Anyone with social media profiles
- Brand ambassadors
- Podcasters, hosts

**❌ EXCLUDED (Not Influencers):**
- Regular employees without influencer roles
- People without social media presence
- Non-marketing/PR roles

## 💡 Best Domains for Influencers:

- `techcrunch.com` - Tech journalists & influencers
- `forbes.com` - Business influencers
- `mashable.com` - Digital media creators
- `theverge.com` - Tech influencers
- `vox.com` - Media personalities
- `buzzfeed.com` - Content creators
- Any media company or marketing agency domain

## 🎯 Result:

You'll get a **clean list of ONLY influencers** with:
- ✅ Job titles that indicate influencer status
- ✅ Social media profiles
- ✅ Contact information
- ✅ Company details
- ✅ All exported to Google Sheets!


