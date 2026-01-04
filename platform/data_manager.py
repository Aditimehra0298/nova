#!/usr/bin/env python3
"""
Influencer Data Manager
Manages influencer data from CSV (primary) and Google Sheets (fallback)
"""

import os
import csv
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional

class InfluencerDataManager:
    """Manage influencer data from CSV (primary) and Google Sheets (fallback)"""
    
    # Path to the main influencer CSV file
    # Try environment variable first, then default relative path
    _default_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Indian_Influencers_Master_List.csv')
    CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', _default_csv_path)
    
    def __init__(self):
        self.spreadsheet = None
        self.worksheet = None
        self.csv_data = None
        self._load_csv_data()
        self._connect_to_sheet()
    
    def _load_csv_data(self):
        """Load influencer data from CSV file (primary source)"""
        try:
            if not os.path.exists(self.CSV_FILE_PATH):
                print(f"⚠️  CSV file not found at: {self.CSV_FILE_PATH}")
                self.csv_data = []
                return
            
            influencers = []
            with open(self.CSV_FILE_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader, 1):
                    # Skip empty rows
                    if not row.get('Name/Brand', '').strip():
                        continue
                    
                    # Map CSV columns to expected format
                    category = row.get('Category', '').strip()
                    domain_niche = row.get('Domain/Niche', '').strip()
                    
                    influencer = {
                        'id': idx,
                        'full_name': row.get('Name/Brand', '').strip(),
                        'email': row.get('Public Email', '').strip(),
                        'industry': category,  # Category from CSV
                        'category': category,  # Also set as category for compatibility
                        'job_title': domain_niche,  # Domain/Niche as job_title
                        'company_name': row.get('Name/Brand', '').strip(),  # Use name as company for brands
                        'location': 'India',  # Default location for Indian influencers
                        'contact_type': row.get('Contact Type', '').strip(),
                        'contact_link': row.get('Contact/Link', '').strip(),
                        'use_case': row.get('What to use for', '').strip(),
                        'source_url': row.get('Source URL', '').strip(),
                        'domain_niche': domain_niche,  # Domain/Niche from CSV
                        # Additional fields for compatibility
                        'bio': f"{domain_niche} - {row.get('What to use for', '').strip()}" if domain_niche else row.get('What to use for', '').strip(),
                        'platform': 'Multiple',  # Default since CSV doesn't specify
                    }
                    influencers.append(influencer)
            
            self.csv_data = influencers
            print(f"✅ Loaded {len(influencers)} influencers from CSV: {os.path.basename(self.CSV_FILE_PATH)}")
        except Exception as e:
            print(f"⚠️  Error loading CSV data: {e}")
            self.csv_data = []
    
    def _connect_to_sheet(self):
        """Connect to Google Sheet (fallback/optional)"""
        try:
            creds_path = os.getenv('GOOGLE_CREDENTIALS_FILE', '../credentials.json')
            
            # Try multiple paths
            if not os.path.exists(creds_path):
                # Try parent directory
                parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
                if os.path.exists(parent_path):
                    creds_path = parent_path
                elif os.path.exists('credentials.json'):
                    creds_path = 'credentials.json'
                else:
                    print(f"⚠️  Google credentials not found. Tried: {creds_path}")
                    return
            
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(creds_path, scopes=scope)
            client = gspread.authorize(creds)
            
            spreadsheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Influencer Data')
            self.spreadsheet = client.open(spreadsheet_name)
            self.worksheet = self.spreadsheet.worksheet('Influencers')
            
            print(f"✅ Connected to Google Sheet: {spreadsheet_name} (fallback)")
        except Exception as e:
            print(f"⚠️  Error connecting to Google Sheet: {e} (using CSV only)")
    
    def get_all_influencers(self) -> List[Dict]:
        """Get all influencers from CSV (primary) and optionally merge with Google Sheets"""
        # Primary source: CSV
        influencers = self.csv_data.copy() if self.csv_data else []
        
        # Optional: Merge with Google Sheets data if available
        if self.worksheet:
            try:
                records = self.worksheet.get_all_records()
                # Add Google Sheets data with offset IDs
                offset = len(influencers)
                for idx, record in enumerate(records, 1):
                    record['id'] = offset + idx
                    record['source'] = 'google_sheets'  # Mark source
                    influencers.append(record)
                print(f"📊 Merged {len(records)} influencers from Google Sheets")
            except Exception as e:
                print(f"⚠️  Error merging Google Sheets data: {e}")
        
        return influencers
    
    def get_influencer_by_id(self, influencer_id: str) -> Optional[Dict]:
        """Get influencer by ID, email, or name"""
        influencers = self.get_all_influencers()
        
        # Try by numeric ID
        try:
            idx = int(influencer_id) - 1
            if 0 <= idx < len(influencers):
                return influencers[idx]
        except:
            pass
        
        # Try by email
        for inf in influencers:
            if inf.get('email', '').lower() == influencer_id.lower():
                return inf
        
        # Try by name
        for inf in influencers:
            if inf.get('full_name', '').lower() == influencer_id.lower():
                return inf
        
        return None
    
    def get_filter_options(self) -> Dict:
        """Get available filter options from data"""
        influencers = self.get_all_influencers()
        
        if not influencers:
            return {
                "industries": [],
                "locations": [],
                "job_titles": [],
                "categories": [],
                "total_influencers": 0
            }
        
        industries = set()
        locations = set()
        job_titles = set()
        categories = set()
        
        for inf in influencers:
            # Industry/Category
            if inf.get('industry'):
                industries.add(inf['industry'])
                categories.add(inf['industry'])
            if inf.get('category'):
                categories.add(inf['category'])
            
            # Location
            if inf.get('location'):
                locations.add(inf['location'])
            if inf.get('country'):
                locations.add(inf['country'])
            
            # Job title / Domain/Niche
            if inf.get('job_title'):
                job_titles.add(inf['job_title'])
            if inf.get('domain_niche'):
                job_titles.add(inf['domain_niche'])
        
        return {
            "industries": sorted(list(industries)),
            "categories": sorted(list(categories)),
            "locations": sorted(list(locations)),
            "job_titles": sorted(list(job_titles)),
            "total_influencers": len(influencers)
        }
    
    def reload_csv_data(self):
        """Reload CSV data (useful when CSV is updated)"""
        self._load_csv_data()
        print("✅ CSV data reloaded")

