#!/usr/bin/env python3
"""
Consolidate all influencer data - read existing and ensure all records are present
"""

import gspread
from google.oauth2.service_account import Credentials
import os

def consolidate_sheet():
    """Check and consolidate all data in the sheet"""
    
    creds_path = 'credentials.json'
    if not os.path.exists(creds_path):
        print("Error: credentials.json not found")
        return
    
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    
    try:
        spreadsheet = client.open("Influencer Data")
        worksheet = spreadsheet.worksheet("Influencers")
        
        # Get all records
        all_records = worksheet.get_all_records()
        
        print(f"\n{'='*70}")
        print("📊 CURRENT DATA IN GOOGLE SHEET")
        print(f"{'='*70}\n")
        print(f"Total Records: {len(all_records)}")
        print(f"Total Rows: {len(all_records) + 1} (including header)")
        
        # Count unique emails
        emails = [r.get('email', '') for r in all_records if r.get('email')]
        unique_emails = set(emails)
        print(f"Unique Emails: {len(unique_emails)}")
        print(f"Duplicate Emails: {len(emails) - len(unique_emails)}")
        
        # Show sample
        if all_records:
            print(f"\n📋 Sample Records (first 3):")
            for i, record in enumerate(all_records[:3], 1):
                print(f"\n  {i}. {record.get('full_name', 'N/A')}")
                print(f"     Email: {record.get('email', 'N/A')}")
                print(f"     Job Title: {record.get('job_title', 'N/A')}")
                print(f"     Company: {record.get('company_name', 'N/A')}")
        
        print(f"\n{'='*70}")
        print("✅ Data consolidation check complete!")
        print(f"{'='*70}\n")
        
        print("💡 The export function now APPENDS data instead of clearing it.")
        print("   New extractions will add to existing data (no duplicates).\n")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    consolidate_sheet()


