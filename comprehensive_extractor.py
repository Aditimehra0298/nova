#!/usr/bin/env python3
"""
Comprehensive Multi-Platform Influencer Extractor
Extracts from multiple domains representing different platforms and industries
"""

import requests
import json
import csv
import time
from typing import List, Dict, Optional
from datetime import datetime
import argparse

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False


class ComprehensiveExtractor:
    """Extract influencers from multiple platforms and domains"""
    
    BASE_URL = "https://api.hunter.io/v2"
    
    # Platform-specific domain lists
    PLATFORM_DOMAINS = {
        'tech_media': [
            'techcrunch.com', 'theverge.com', 'wired.com', 'arstechnica.com',
            'engadget.com', 'gizmodo.com', 'mashable.com', 'venturebeat.com'
        ],
        'business_media': [
            'forbes.com', 'bloomberg.com', 'wsj.com', 'ft.com',
            'businessinsider.com', 'cnbc.com', 'reuters.com'
        ],
        'marketing': [
            'hubspot.com', 'marketingland.com', 'adweek.com', 'adage.com',
            'socialmediaexaminer.com', 'contentmarketinginstitute.com'
        ],
        'social_media_companies': [
            'linkedin.com', 'twitter.com', 'meta.com', 'snap.com',
            'tiktok.com', 'pinterest.com'
        ],
        'influencer_platforms': [
            'influencermarketinghub.com', 'grin.co', 'aspireiq.com',
            'upfluence.com', 'klear.com'
        ],
        'content_creators': [
            'medium.com', 'substack.com', 'ghost.org', 'wordpress.com'
        ]
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.rate_limit_delay = 0.067
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """Make API request"""
        self._rate_limit()
        params['api_key'] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    def search_domain(self, domain: str, limit: int = 10) -> List[Dict]:
        """Search a domain for contacts"""
        print(f"  Searching: {domain}")
        response = self._make_request("domain-search", {
            "domain": domain,
            "limit": limit
        })
        
        if response and response.get('data') and response['data'].get('emails'):
            emails = response['data']['emails']
            results = []
            for email_data in emails:
                results.append({
                    'platform': self._identify_platform(domain),
                    'domain': domain,
                    'email': email_data.get('value', ''),
                    'full_name': f"{email_data.get('first_name', '')} {email_data.get('last_name', '')}".strip(),
                    'first_name': email_data.get('first_name', ''),
                    'last_name': email_data.get('last_name', ''),
                    'job_title': email_data.get('position', ''),
                    'linkedin_handle': email_data.get('linkedin', ''),
                    'twitter_handle': email_data.get('twitter', ''),
                    'source': f'Hunter.io - {domain}'
                })
            print(f"    Found {len(results)} contacts")
            return results
        return []
    
    def _identify_platform(self, domain: str) -> str:
        """Identify platform category from domain"""
        domain_lower = domain.lower()
        
        if any(d in domain_lower for d in ['techcrunch', 'theverge', 'wired', 'ars', 'engadget', 'gizmodo', 'mashable']):
            return 'Tech Media'
        elif any(d in domain_lower for d in ['forbes', 'bloomberg', 'wsj', 'ft', 'businessinsider', 'cnbc', 'reuters']):
            return 'Business Media'
        elif any(d in domain_lower for d in ['hubspot', 'marketingland', 'adweek', 'adage', 'socialmedia', 'contentmarketing']):
            return 'Marketing'
        elif any(d in domain_lower for d in ['linkedin', 'twitter', 'meta', 'snap', 'tiktok', 'pinterest']):
            return 'Social Media Platform'
        elif any(d in domain_lower for d in ['influencer', 'grin', 'aspire', 'upfluence', 'klear']):
            return 'Influencer Platform'
        elif any(d in domain_lower for d in ['medium', 'substack', 'ghost', 'wordpress']):
            return 'Content Platform'
        else:
            return 'Other'
    
    def search_platforms(self, platform_types: List[str] = None, limit_per_domain: int = 10) -> List[Dict]:
        """Search across multiple platform types"""
        if platform_types is None:
            platform_types = list(self.PLATFORM_DOMAINS.keys())
        
        all_results = []
        
        for platform_type in platform_types:
            if platform_type not in self.PLATFORM_DOMAINS:
                continue
            
            print(f"\n{'='*60}")
            print(f"Searching {platform_type.replace('_', ' ').title()} Platforms")
            print(f"{'='*60}")
            
            domains = self.PLATFORM_DOMAINS[platform_type]
            for domain in domains:
                results = self.search_domain(domain, limit=limit_per_domain)
                all_results.extend(results)
                time.sleep(1)  # Be respectful
        
        return all_results
    
    def search_custom_domains(self, domains: List[str], limit_per_domain: int = 10) -> List[Dict]:
        """Search custom list of domains"""
        all_results = []
        
        for domain in domains:
            results = self.search_domain(domain, limit=limit_per_domain)
            all_results.extend(results)
        
        return all_results
    
    def filter_influencers(self, profiles: List[Dict]) -> List[Dict]:
        """Filter for influencers"""
        influencer_keywords = [
            'influencer', 'content creator', 'creator', 'blogger', 'vlogger',
            'youtuber', 'social media', 'social media manager', 'community manager',
            'marketing', 'brand ambassador', 'ambassador', 'public relations', 'pr',
            'journalist', 'reporter', 'editor', 'writer', 'author', 'columnist',
            'podcaster', 'host', 'presenter', 'correspondent', 'analyst'
        ]
        
        filtered = []
        for profile in profiles:
            job_title = str(profile.get('job_title', '')).lower()
            has_social = bool(profile.get('linkedin_handle') or profile.get('twitter_handle'))
            
            is_influencer = any(keyword in job_title for keyword in influencer_keywords)
            
            if is_influencer or has_social:
                filtered.append(profile)
        
        return filtered
    
    def _flatten_data(self, data: List[Dict]) -> List[Dict]:
        """Flatten data for export"""
        flattened = []
        for record in data:
            flat = {
                'platform': record.get('platform', ''),
                'domain': record.get('domain', ''),
                'email': record.get('email', ''),
                'full_name': record.get('full_name', ''),
                'first_name': record.get('first_name', ''),
                'last_name': record.get('last_name', ''),
                'job_title': record.get('job_title', ''),
                'linkedin_handle': record.get('linkedin_handle', ''),
                'linkedin_url': f"https://linkedin.com/in/{record.get('linkedin_handle', '')}" if record.get('linkedin_handle') else '',
                'twitter_handle': record.get('twitter_handle', ''),
                'twitter_url': f"https://twitter.com/{record.get('twitter_handle', '')}" if record.get('twitter_handle') else '',
                'source': record.get('source', ''),
            }
            flattened.append(flat)
        return flattened
    
    def export_to_csv(self, data: List[Dict], filename: str):
        """Export to CSV"""
        if not data:
            return
        
        flattened = self._flatten_data(data)
        fieldnames = flattened[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened)
        
        print(f"\n✅ Exported {len(flattened)} records to {filename}")
    
    def export_to_google_sheets(self, data: List[Dict], spreadsheet_name: str,
                                worksheet_name: str = 'Influencers',
                                credentials_file: Optional[str] = None):
        """Export to Google Sheets"""
        if not GOOGLE_SHEETS_AVAILABLE:
            print("Error: Install gspread and google-auth")
            return
        
        if not data:
            return
        
        try:
            import os
            creds_path = credentials_file or os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
            
            if not os.path.exists(creds_path):
                print(f"Error: Google credentials not found")
                return
            
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(creds_path, scopes=scope)
            client = gspread.authorize(creds)
            
            try:
                spreadsheet = client.open(spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                spreadsheet = client.create(spreadsheet_name)
            
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
                # Get existing data to avoid duplicates
                existing_data = worksheet.get_all_records()
                existing_emails = {row.get('email', '').lower() for row in existing_data if row.get('email')}
                print(f"Found {len(existing_data)} existing records")
            except:
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=10000, cols=30)
                existing_emails = set()
                print(f"Created new worksheet: {worksheet_name}")
            
            flattened = self._flatten_data(data)
            
            # Filter out duplicates
            new_data = []
            for record in flattened:
                email = record.get('email', '').lower()
                if email and email not in existing_emails:
                    new_data.append(record)
                    existing_emails.add(email)
            
            if not new_data:
                print("No new records to add (all duplicates)")
                return
            
            headers = list(flattened[0].keys())
            
            # If worksheet is empty, write headers first
            try:
                existing_headers = worksheet.row_values(1)
                if not existing_headers:
                    worksheet.append_row(headers)
            except:
                worksheet.append_row(headers)
            
            # Append new rows
            print(f"Adding {len(new_data)} new records...")
            for record in new_data:
                row = [record.get(header, '') for header in headers]
                worksheet.append_row(row)
            
            worksheet.format('A1:Z1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            print(f"\n✅ Exported {len(flattened)} records to Google Sheets")
            print(f"   URL: {spreadsheet.url}")
            
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive Multi-Platform Influencer Extractor'
    )
    parser.add_argument('--api-key', type=str, required=True,
                       help='Hunter.io API key')
    parser.add_argument('--platforms', type=str,
                       help='Platform types: tech_media,business_media,marketing,social_media_companies,influencer_platforms,content_creators (or "all")')
    parser.add_argument('--domains', type=str,
                       help='Custom comma-separated domains to search')
    parser.add_argument('--format', type=str, choices=['csv', 'gsheet', 'both'],
                       default='gsheet', help='Output format')
    parser.add_argument('--google-sheet', type=str,
                       help='Google Sheet name')
    parser.add_argument('--google-worksheet', type=str, default='Influencers',
                       help='Google Worksheet tab name')
    parser.add_argument('--output', type=str, default='influencer_data',
                       help='Output filename')
    parser.add_argument('--limit', type=int, default=10,
                       help='Limit per domain (default: 10)')
    parser.add_argument('--no-filter', action='store_true',
                       help='Disable influencer filtering')
    
    args = parser.parse_args()
    
    extractor = ComprehensiveExtractor(args.api_key)
    all_results = []
    
    # Search platform types
    if args.platforms:
        if args.platforms.lower() == 'all':
            platform_types = list(extractor.PLATFORM_DOMAINS.keys())
        else:
            platform_types = [p.strip() for p in args.platforms.split(',')]
        
        print(f"\n{'='*60}")
        print("🚀 Comprehensive Multi-Platform Influencer Extraction")
        print(f"{'='*60}\n")
        
        results = extractor.search_platforms(platform_types, limit_per_domain=args.limit)
        all_results.extend(results)
    
    # Search custom domains
    if args.domains:
        domains = [d.strip() for d in args.domains.split(',')]
        results = extractor.search_custom_domains(domains, limit_per_domain=args.limit)
        all_results.extend(results)
    
    if not all_results:
        print("Error: Please provide platforms or domains to search")
        return
    
    # Filter influencers
    if not args.no_filter:
        print(f"\n🔍 Filtering {len(all_results)} profiles for influencers...")
        all_results = extractor.filter_influencers(all_results)
        print(f"✅ Found {len(all_results)} influencers")
    
    # Export
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if args.format in ['csv', 'both']:
        filename = f"{args.output}_{timestamp}.csv"
        extractor.export_to_csv(all_results, filename)
    
    if args.format in ['gsheet', 'both']:
        sheet_name = args.google_sheet or 'Influencer Data'
        extractor.export_to_google_sheets(
            all_results,
            spreadsheet_name=sheet_name,
            worksheet_name=args.google_worksheet
        )
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully extracted {len(all_results)} influencer profiles")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

