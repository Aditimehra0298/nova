#!/usr/bin/env python3
"""
Import CSV influencer data into Google Sheets
"""

import csv
import os
import sys
from data_manager import InfluencerDataManager
import gspread
from google.oauth2.service_account import Credentials

def import_csv_to_sheet(csv_file_path, sheet_name='Influencer Data'):
    """Import CSV data into Google Sheet"""
    
    # Connect to Google Sheet
    try:
        creds_path = os.getenv('GOOGLE_CREDENTIALS_FILE', '../credentials.json')
        
        if not os.path.exists(creds_path):
            parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
            if os.path.exists(parent_path):
                creds_path = parent_path
            elif os.path.exists('credentials.json'):
                creds_path = 'credentials.json'
            else:
                print(f"❌ Google credentials not found. Tried: {creds_path}")
                return False
        
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        
        spreadsheet = client.open(sheet_name)
        
        # Try to get existing worksheet or create new
        try:
            worksheet = spreadsheet.worksheet('Influencers')
        except:
            worksheet = spreadsheet.add_worksheet(title='Influencers', rows=1000, cols=20)
        
        print(f"✅ Connected to Google Sheet: {sheet_name}")
        
    except Exception as e:
        print(f"❌ Error connecting to Google Sheet: {e}")
        return False
    
    # Read CSV file
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file not found: {csv_file_path}")
        return False
    
    print(f"📖 Reading CSV file: {csv_file_path}")
    
    influencers = []
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map CSV columns to sheet format
            influencer = {
                'full_name': row.get('name', ''),
                'username': row.get('username', ''),
                'email': row.get('email', '') or f"{row.get('username', '')}@example.com",
                'profile_url': row.get('profile_url', ''),
                'followers': row.get('followers', ''),
                'platform': row.get('platform', '').lower(),
                'location': row.get('location', ''),
                'source': row.get('source', ''),
                'job_title': '',  # Will be inferred from platform/username
                'company_name': '',
                'industry': '',
                'bio': f"Influencer on {row.get('platform', '')}",
            }
            
            # Set platform-specific handles
            platform = row.get('platform', '').lower()
            profile_url = row.get('profile_url', '')
            
            if platform == 'instagram':
                influencer['instagram_handle'] = row.get('username', '')
                influencer['instagram_url'] = profile_url
            elif platform == 'twitter':
                influencer['twitter_handle'] = row.get('username', '')
                influencer['twitter_url'] = profile_url
            elif platform == 'linkedin':
                influencer['linkedin_handle'] = row.get('username', '')
                influencer['linkedin_url'] = profile_url
            elif platform == 'facebook':
                influencer['facebook_handle'] = row.get('username', '')
                influencer['facebook_url'] = profile_url
            elif platform == 'youtube':
                influencer['youtube_handle'] = row.get('username', '')
                influencer['youtube_url'] = profile_url
            
            # Infer job title from username/name
            username = row.get('username', '').lower()
            if 'influencer' in username:
                influencer['job_title'] = 'Influencer'
            elif 'blogger' in username:
                influencer['job_title'] = 'Blogger'
            elif 'creator' in username:
                influencer['job_title'] = 'Content Creator'
            elif 'vlogger' in username:
                influencer['job_title'] = 'Vlogger'
            elif 'fashion' in username:
                influencer['job_title'] = 'Fashion Influencer'
                influencer['industry'] = 'Fashion'
            elif 'food' in username or 'foodie' in username:
                influencer['job_title'] = 'Food Influencer'
                influencer['industry'] = 'Food & Beverage'
            elif 'travel' in username or 'traveler' in username:
                influencer['job_title'] = 'Travel Influencer'
                influencer['industry'] = 'Travel'
            elif 'fitness' in username:
                influencer['job_title'] = 'Fitness Influencer'
                influencer['industry'] = 'Fitness & Health'
            elif 'beauty' in username:
                influencer['job_title'] = 'Beauty Influencer'
                influencer['industry'] = 'Beauty'
            elif 'tech' in username:
                influencer['job_title'] = 'Tech Influencer'
                influencer['industry'] = 'Technology'
            elif 'comedy' in username:
                influencer['job_title'] = 'Comedian'
                influencer['industry'] = 'Entertainment'
            else:
                influencer['job_title'] = 'Influencer'
            
            influencers.append(influencer)
    
    print(f"📊 Found {len(influencers)} influencers in CSV")
    
    # Get existing data to avoid duplicates
    try:
        existing_records = worksheet.get_all_records()
        existing_emails = {r.get('email', '').lower() for r in existing_records if r.get('email')}
        existing_usernames = {r.get('username', '').lower() for r in existing_records if r.get('username')}
    except:
        existing_emails = set()
        existing_usernames = set()
    
    # Filter out duplicates
    new_influencers = []
    for inf in influencers:
        email = inf.get('email', '').lower()
        username = inf.get('username', '').lower()
        
        if email not in existing_emails and username not in existing_usernames:
            new_influencers.append(inf)
            existing_emails.add(email)
            existing_usernames.add(username)
    
    print(f"✨ {len(new_influencers)} new influencers to add (skipped {len(influencers) - len(new_influencers)} duplicates)")
    
    if not new_influencers:
        print("✅ No new influencers to add")
        return True
    
    # Prepare headers
    headers = [
        'full_name', 'username', 'email', 'job_title', 'company_name', 'industry',
        'location', 'bio', 'followers',
        'linkedin_handle', 'linkedin_url',
        'twitter_handle', 'twitter_url',
        'instagram_handle', 'instagram_url',
        'youtube_handle', 'youtube_url',
        'facebook_handle', 'facebook_url',
        'profile_url', 'platform', 'source'
    ]
    
    # Check if headers exist
    try:
        existing_headers = worksheet.row_values(1)
        if not existing_headers or existing_headers[0] != 'full_name':
            worksheet.insert_row(headers, 1)
            print("✅ Added headers")
    except:
        worksheet.insert_row(headers, 1)
        print("✅ Added headers")
    
    # Prepare data rows
    rows_to_add = []
    for inf in new_influencers:
        row = [inf.get(h, '') for h in headers]
        rows_to_add.append(row)
    
    # Append rows in batches
    batch_size = 100
    for i in range(0, len(rows_to_add), batch_size):
        batch = rows_to_add[i:i+batch_size]
        worksheet.append_rows(batch)
        print(f"✅ Added batch {i//batch_size + 1} ({len(batch)} influencers)")
    
    print(f"\n🎉 Successfully imported {len(new_influencers)} influencers!")
    print(f"📊 Total influencers in sheet: {len(existing_records) + len(new_influencers)}")
    
    return True

if __name__ == '__main__':
    # Find CSV file
    csv_file = '800_influencers_balanced.csv'
    
    # Try multiple locations
    possible_paths = [
        csv_file,
        f'../{csv_file}',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), csv_file),
        os.path.join(os.path.dirname(__file__), csv_file)
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        print(f"❌ CSV file not found. Tried: {possible_paths}")
        sys.exit(1)
    
    print(f"📁 Using CSV file: {csv_path}\n")
    
    success = import_csv_to_sheet(csv_path)
    
    if success:
        print("\n✅ Import complete!")
    else:
        print("\n❌ Import failed!")
        sys.exit(1)


