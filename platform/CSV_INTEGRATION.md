# CSV Integration Guide

## Overview

The platform now uses `Indian_Influencers_Master_List.csv` as the **primary source** for influencer recommendations. When clients put in requirements, the system shows recommendations from this CSV file.

## How It Works

### Data Loading
- The CSV file is automatically loaded when the platform starts
- Location: `/Users/aditimehra/Documents/nova/Indian_Influencers_Master_List.csv`
- The system maps CSV columns to the expected influencer format:
  - `Category` → `industry`
  - `Name/Brand` → `full_name` and `company_name`
  - `Domain/Niche` → `job_title` and `domain_niche`
  - `Public Email` → `email`
  - `Contact Type` → `contact_type`
  - `Contact/Link` → `contact_link`
  - `What to use for` → `use_case`
  - `Source URL` → `source_url`

### Adding More Influencers

Simply add new rows to `Indian_Influencers_Master_List.csv` with the same column structure:

```csv
Category,Name/Brand,Domain/Niche,Public Email,Contact Type,Contact/Link,What to use for,Source URL
Your Category,Influencer Name,Their Domain/Niche,email@example.com,Contact Type,https://contact-link.com,Use case description,https://source-url.com
```

### Reloading CSV Data

After updating the CSV file, you can reload the data in two ways:

1. **Restart the server** - The CSV is automatically reloaded on startup
2. **Use the API endpoint** - Send a POST request to `/api/reload-csv`

### Recommendation System

When clients enter requirements:
- **Industry/Category filter**: Matches against the `Category` column
- **Location filter**: Defaults to "India" for all CSV influencers
- **Content Type filter**: Matches against `Domain/Niche` and `What to use for`
- **Target Audience filter**: Matches against `Domain/Niche` and `What to use for`

### Display Fields

The frontend now displays:
- Category/Industry
- Domain/Niche
- Contact Type
- Contact Link (clickable)
- Use Case
- Source URL (clickable)
- Email (clickable mailto link)

## Testing

To verify the integration is working:

```bash
cd platform
python3 -c "from data_manager import InfluencerDataManager; dm = InfluencerDataManager(); print(f'Loaded {len(dm.get_all_influencers())} influencers')"
```

## Notes

- The CSV is the **primary source** - it loads first
- Google Sheets data (if available) is merged as a fallback/secondary source
- All influencers from the CSV are automatically included in recommendations
- The system handles missing fields gracefully

