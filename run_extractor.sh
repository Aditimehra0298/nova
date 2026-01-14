#!/bin/bash
# Quick script to run the Hunter.io extractor and export to Google Sheets

# Set your Hunter.io API key here, or use environment variable
# export HUNTER_API_KEY="your_api_key_here"

# Set your Google Sheet name (must match exactly)
GOOGLE_SHEET_NAME="Influencer Data"

# Run the extractor
python3 hunter_extractor.py \
  --api-key "${HUNTER_API_KEY:-$1}" \
  --domains "${2:-techcrunch.com}" \
  --format gsheet \
  --google-sheet "$GOOGLE_SHEET_NAME" \
  --google-worksheet "Influencers" \
  --limit 50

echo ""
echo "✅ Done! Check your Google Sheet: $GOOGLE_SHEET_NAME"


