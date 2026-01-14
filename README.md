# Hunter.io Influencer Data Extractor

A Python tool to extract comprehensive influencer data from Hunter.io using their API. This tool can enrich email addresses, LinkedIn profiles, and search domains for influencer contacts.

## Features

- ✅ **Email Enrichment**: Enrich individual or bulk email addresses with full profile data
- ✅ **LinkedIn Enrichment**: Extract data from LinkedIn profile handles
- ✅ **Domain Search**: Search for influencers within specific domains
- ✅ **Bulk Processing**: Process multiple emails/domains efficiently
- ✅ **Rate Limiting**: Automatically handles API rate limits (15 req/sec, 500 req/min)
- ✅ **Multiple Export Formats**: Export to JSON, CSV, Google Sheets, or both
- ✅ **Google Sheets Integration**: Direct export to Google Sheets with automatic formatting
- ✅ **Comprehensive Data**: Extracts name, location, social media, employment, and more

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. **Get your Hunter.io API Key**:
   - Sign up at [hunter.io](https://hunter.io)
   - Navigate to your account settings → API section
   - Copy your API key

2. **Set your API key** (choose one method):
   - Set environment variable: `export HUNTER_API_KEY=your_api_key_here`
   - Or pass it via command line: `--api-key your_api_key_here`

3. **For Google Sheets Export** (optional):
   - Follow the setup guide in `GOOGLE_SHEETS_SETUP.md`
   - Download Google Service Account credentials JSON file
   - Save as `credentials.json` in the project directory

## Usage

### Basic Examples

#### 1. Enrich a single email address
```bash
python hunter_extractor.py --api-key YOUR_API_KEY --emails "influencer@example.com" --format both
```

#### 2. Enrich multiple emails
```bash
python hunter_extractor.py --api-key YOUR_API_KEY --emails "email1@example.com,email2@example.com,email3@example.com" --format csv
```

#### 3. Enrich emails from a file
```bash
python hunter_extractor.py --api-key YOUR_API_KEY --emails-file emails.txt --format both
```

#### 4. Search a domain for influencers
```bash
python hunter_extractor.py --api-key YOUR_API_KEY --domains "techcrunch.com,forbes.com" --limit 50 --format csv
```

#### 5. Search multiple domains from a file
```bash
python hunter_extractor.py --api-key YOUR_API_KEY --domains-file domains.txt --limit 100 --format both
```

#### 6. Enrich LinkedIn profiles
```bash
python hunter_extractor.py --api-key YOUR_API_KEY --linkedin "john-doe,jane-smith" --format json
```

#### 7. Export to Google Sheets
```bash
python hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains "techcrunch.com,forbes.com" \
  --format gsheet \
  --google-sheet "Influencer Data" \
  --google-worksheet "Influencers" \
  --google-credentials credentials.json
```

#### 8. Combined approach
```bash
python hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --emails-file emails.txt \
  --domains "example.com,another.com" \
  --format both \
  --output influencer_data
```

### Command Line Options

- `--api-key`: Your Hunter.io API key (or set HUNTER_API_KEY env var)
- `--emails`: Comma-separated list of emails to enrich
- `--emails-file`: File containing emails (one per line)
- `--linkedin`: Comma-separated list of LinkedIn handles
- `--domains`: Comma-separated list of domains to search
- `--domains-file`: File containing domains (one per line)
- `--output`: Output filename prefix (default: "influencer_data")
- `--format`: Output format - `json`, `csv`, `both`, or `gsheet` (default: both)
- `--limit`: Maximum results per domain (default: 100)
- `--google-sheet`: Google Sheet name (required for gsheet format)
- `--google-worksheet`: Google Worksheet tab name (default: "Influencers")
- `--google-credentials`: Path to Google Service Account credentials JSON file (default: "credentials.json")

### Example Input Files

**emails.txt:**
```
influencer1@example.com
influencer2@example.com
influencer3@example.com
```

**domains.txt:**
```
techcrunch.com
forbes.com
mashable.com
```

## Output Format

### JSON Output
Full nested structure with all available data:
```json
{
  "email": "john@example.com",
  "name": {
    "fullName": "John Doe",
    "givenName": "John",
    "familyName": "Doe"
  },
  "location": "New York, NY, United States",
  "employment": {
    "name": "Example Inc.",
    "title": "Marketing Manager"
  },
  "linkedin": {
    "handle": "john-doe"
  },
  ...
}
```

### CSV Output
Flattened structure with columns:
- email, full_name, first_name, last_name
- location, city, state, country, timezone
- company_name, company_domain, job_title, role, seniority
- linkedin_handle, twitter_handle, facebook_handle, instagram_handle, youtube_handle
- bio, avatar_url, phone_number

## API Rate Limits

The tool automatically handles Hunter.io's rate limits:
- **15 requests per second**
- **500 requests per minute**

The script includes built-in rate limiting to prevent API errors.

## Data Extracted

For each influencer, the tool extracts:
- ✅ Full name and personal details
- ✅ Email address
- ✅ Location (city, state, country, coordinates)
- ✅ Timezone
- ✅ Employment information (company, title, role, seniority)
- ✅ Social media profiles (LinkedIn, Twitter, Facebook, Instagram, YouTube)
- ✅ Bio and avatar
- ✅ Phone number (when available)

## Error Handling

- Invalid API keys are caught and reported
- Failed enrichments are logged but don't stop the process
- Network errors are handled gracefully
- Rate limits are automatically respected

## Examples

### Example 1: Extract influencers from tech blogs
```bash
python hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains "techcrunch.com,venturebeat.com,theverge.com" \
  --limit 50 \
  --format both \
  --output tech_influencers
```

### Example 2: Enrich a list of known influencer emails
```bash
python hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --emails-file known_influencers.txt \
  --format csv \
  --output enriched_profiles
```

### Example 3: Find influencers in marketing agencies
```bash
python hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains-file marketing_agencies.txt \
  --limit 100 \
  --format both
```

### Example 4: Export directly to Google Sheets
```bash
python hunter_extractor.py \
  --api-key YOUR_API_KEY \
  --domains "techcrunch.com,venturebeat.com" \
  --format gsheet \
  --google-sheet "Tech Influencers 2024" \
  --google-worksheet "Data" \
  --limit 50
```

## Notes

- Hunter.io API requires a paid plan for most features
- Free tier has limited requests per month
- Some data fields may be empty depending on availability
- Domain search results may include non-influencer contacts

## License

This tool is provided as-is for data extraction purposes. Please ensure you comply with Hunter.io's Terms of Service and API usage policies.

## Google Sheets Export

To export directly to Google Sheets:

1. **Setup Google Sheets API** (see `GOOGLE_SHEETS_SETUP.md` for detailed instructions):
   - Create a Google Cloud project
   - Enable Google Sheets API and Google Drive API
   - Create a Service Account and download credentials JSON
   - Save as `credentials.json`

2. **Export to Google Sheets**:
   ```bash
   python hunter_extractor.py \
     --api-key YOUR_API_KEY \
     --domains "example.com" \
     --format gsheet \
     --google-sheet "My Influencer Data"
   ```

The script will:
- Create a new Google Sheet (or use existing if shared)
- Format headers with bold text and background color
- Auto-resize columns
- Provide the sheet URL in the output

## Support

For issues with:
- **This tool**: Check the code or create an issue
- **Hunter.io API**: Visit [hunter.io/api-documentation](https://hunter.io/api-documentation)
- **Google Sheets Setup**: See `GOOGLE_SHEETS_SETUP.md`

# nova
