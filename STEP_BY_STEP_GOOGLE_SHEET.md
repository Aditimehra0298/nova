# Step-by-Step: Using an Existing Google Sheet

## Step 1: Create a New Google Sheet

1. **Open Google Sheets**
   - Go to [sheets.google.com](https://sheets.google.com)
   - Or go to [drive.google.com](https://drive.google.com) and click "New" → "Google Sheets"

2. **Create a blank spreadsheet**
   - Click on "Blank" to create a new sheet
   - Or use the template if you prefer

3. **Name your sheet**
   - Click on "Untitled spreadsheet" at the top
   - Enter a name like: `Influencer Data` or `Hunter.io Influencers`
   - Press Enter

## Step 2: Share the Sheet with Service Account

1. **Click the "Share" button**
   - Look for the blue "Share" button in the top-right corner
   - Click it

2. **Add the service account email**
   - In the "Add people and groups" field, paste this email:
     ```
     hunter-extractor@hunter-extractor.iam.gserviceaccount.com
     ```
   - **Important:** Make sure you copy the entire email address

3. **Set permissions**
   - Click the dropdown next to the email (it will say "Viewer" by default)
   - Change it to **"Editor"**
   - This allows the script to write data to the sheet

4. **Share**
   - Click the "Send" button (or just press Enter)
   - You can uncheck "Notify people" if you don't want an email sent
   - The service account doesn't need email notifications

## Step 3: Verify the Sheet Name

1. **Check the exact name**
   - Look at the top of your Google Sheet
   - Note the exact name (case-sensitive)
   - Example: `Influencer Data` or `My Influencers`

## Step 4: Use the Sheet with the Script

Now you can use your sheet with the extractor script!

### Example Command:

```bash
python3 hunter_extractor.py \
  --api-key YOUR_HUNTER_API_KEY \
  --domains "techcrunch.com" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --google-worksheet "Influencers"
```

**Important:** 
- Replace `YOUR_HUNTER_API_KEY` with your actual Hunter.io API key
- Replace `"Influencer Data"` with the exact name of your Google Sheet
- The script will create a worksheet tab called "Influencers" (or use `--google-worksheet` to change it)

## Step 5: View Your Data

1. **Refresh your Google Sheet**
   - Go back to your Google Sheet in the browser
   - Refresh the page (F5 or Cmd+R)
   - You should see the data appear in the "Influencers" tab

2. **Check the data**
   - Headers will be in the first row (bold, gray background)
   - Data will appear in rows below

## Troubleshooting

### If you get "Spreadsheet not found" error:
- Make sure you shared the sheet with the service account email
- Check that the sheet name matches exactly (including capitalization)
- Make sure you gave "Editor" permissions, not "Viewer"

### If data doesn't appear:
- Refresh the Google Sheet page
- Check that the script completed successfully
- Look for the "Influencers" worksheet tab (it might be created automatically)

### To find your sheet later:
- Go to [drive.google.com](https://drive.google.com)
- Look for the sheet name you created
- Or check the URL that the script prints when it finishes


