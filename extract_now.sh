#!/bin/bash
# Quick extraction script

echo "🚀 Starting Influencer Data Extraction..."
echo ""

# Check if API key provided
if [ -z "$1" ]; then
    echo "❌ Error: Hunter.io API key required"
    echo ""
    echo "Usage: ./extract_now.sh YOUR_API_KEY [domain1,domain2] [sheet_name]"
    echo ""
    echo "Example:"
    echo "  ./extract_now.sh abc123xyz techcrunch.com,forbes.com \"Influencer Data\""
    echo ""
    exit 1
fi

API_KEY="$1"
DOMAINS="${2:-techcrunch.com,forbes.com}"
SHEET_NAME="${3:-Influencer Data}"

echo "📊 Extracting from domains: $DOMAINS"
echo "📝 Google Sheet: $SHEET_NAME"
echo ""

python3 hunter_extractor.py \
  --api-key "$API_KEY" \
  --domains "$DOMAINS" \
  --format gsheet \
  --google-sheet "$SHEET_NAME" \
  --google-worksheet "Influencers" \
  --limit 50

echo ""
echo "✅ Extraction complete! Check your Google Sheet."


