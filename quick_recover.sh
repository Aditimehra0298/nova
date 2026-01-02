#!/bin/bash
# Quick recovery script - extract from multiple domains

API_KEY="5c1e38a60d83acdffe5640bd3d17de2980861376"

echo "🔄 Recovering influencer data..."
echo ""

# Extract from tech media
echo "📊 Extracting from Tech Media..."
python3 hunter_extractor.py \
  --api-key "$API_KEY" \
  --domains "techcrunch.com,forbes.com,mashable.com,theverge.com,wired.com" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --limit 10

echo ""
echo "⏳ Waiting 30 seconds..."
sleep 30

# Extract from business media
echo "📊 Extracting from Business Media..."
python3 hunter_extractor.py \
  --api-key "$API_KEY" \
  --domains "bloomberg.com,wsj.com,ft.com,businessinsider.com,cnbc.com" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --limit 10

echo ""
echo "⏳ Waiting 30 seconds..."
sleep 30

# Extract from marketing
echo "📊 Extracting from Marketing..."
python3 hunter_extractor.py \
  --api-key "$API_KEY" \
  --domains "hubspot.com,marketingland.com,adweek.com,adage.com" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --limit 10

echo ""
echo "✅ Recovery complete! Check your Google Sheet."


