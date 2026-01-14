# Google Sheets Setup Guide

This guide will help you set up Google Sheets export functionality for the Hunter.io Influencer Extractor.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "Hunter Extractor")
4. Click "Create"

## Step 2: Enable Required APIs

1. In your project, go to **APIs & Services** → **Library**
2. Search for and enable:
   - **Google Sheets API**
   - **Google Drive API**

## Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Enter a name (e.g., "hunter-extractor")
4. Click **Create and Continue**
5. Skip the optional steps and click **Done**

## Step 4: Create and Download Credentials

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Select **JSON** format
5. Click **Create** - this will download a JSON file
6. **Save this file** as `credentials.json` in the same directory as `hunter_extractor.py`

## Step 5: Share Google Sheet (Optional)

If you want to use an existing Google Sheet:

1. Open your Google Sheet
2. Click **Share** button
3. Add the service account email (found in `credentials.json` as `client_email`)
4. Give it **Editor** permissions
5. Click **Send**

**Note:** If creating a new sheet, the script will create it automatically, but you may need to share it with your personal Google account to view it.

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Use Google Sheets Export

```bash
python hunter_extractor.py \
  --api-key YOUR_HUNTER_API_KEY \
  --domains "example.com" \
  --format gsheet \
  --google-sheet "My Influencer Data" \
  --google-worksheet "Influencers" \
  --google-credentials credentials.json
```

## Troubleshooting

### Error: "Spreadsheet not found"
- Make sure you've shared the spreadsheet with the service account email
- Or let the script create a new spreadsheet automatically

### Error: "Credentials file not found"
- Make sure `credentials.json` is in the same directory
- Or specify the path with `--google-credentials /path/to/credentials.json`

### Error: "API not enabled"
- Go back to Google Cloud Console
- Enable Google Sheets API and Google Drive API

### Can't see the created spreadsheet
- The spreadsheet is created by the service account
- Share it with your personal Google account email
- Or check the service account's Google Drive

## Security Note

**Never commit `credentials.json` to version control!**
- It's already in `.gitignore`
- Keep your credentials file secure
- Don't share it publicly


