#!/bin/bash
# Example script for exporting to Google Sheets

# Make sure you have:
# 1. Hunter.io API key
# 2. Google credentials.json file (see GOOGLE_SHEETS_SETUP.md)

python hunter_extractor.py \
  --api-key "$HUNTER_API_KEY" \
  --domains "techcrunch.com,forbes.com" \
  --format gsheet \
  --google-sheet "Influencer Data $(date +%Y-%m-%d)" \
  --google-worksheet "Influencers" \
  --limit 50


