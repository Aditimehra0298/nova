#!/usr/bin/env python3
"""
Free Influencer Data Extractor
Uses web scraping and public data sources - NO paid APIs required!
"""

import requests
import json
import csv
import time
import re
from typing import List, Dict, Optional
from datetime import datetime
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False


class FreeInfluencerExtractor:
    """Extract influencer data using free methods"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.delay = 2  # Be respectful with delays
    
    def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage"""
        try:
            time.sleep(self.delay)  # Be respectful
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            return None
    
    def extract_emails_from_text(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        # Filter out common non-personal emails
        exclude = ['noreply', 'no-reply', 'donotreply', 'support', 'info', 'contact', 
                  'hello', 'admin', 'webmaster', 'postmaster', 'mailer-daemon']
        return [e for e in emails if not any(x in e.lower() for x in exclude)]
    
    def extract_from_contact_page(self, domain: str) -> List[Dict]:
        """Extract contact information from company contact page"""
        results = []
        contact_urls = [
            f"https://{domain}/contact",
            f"https://{domain}/about",
            f"https://{domain}/team",
            f"https://{domain}/staff",
            f"https://www.{domain}/contact",
        ]
        
        for url in contact_urls:
            print(f"  Checking: {url}")
            soup = self._get_page(url)
            if not soup:
                continue
            
            text = soup.get_text()
            emails = self.extract_emails_from_text(text)
            
            # Look for names near emails
            for email in emails:
                # Try to find name in nearby text
                email_index = text.find(email)
                if email_index > 0:
                    context = text[max(0, email_index-100):email_index+100]
                    # Simple name extraction (can be improved)
                    name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', context)
                    name = name_match.group(1) if name_match else ""
                    
                    results.append({
                        'email': email,
                        'full_name': name,
                        'source': url,
                        'domain': domain
                    })
        
        return results
    
    def search_google_for_contacts(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Google for contact information (using public search)"""
        results = []
        # Note: This is a basic implementation. For production, consider using
        # Google Custom Search API (free tier: 100 queries/day)
        print(f"  Searching Google for: {query}")
        # This would require Google Custom Search API for better results
        return results
    
    def extract_from_linkedin_public(self, company_name: str) -> List[Dict]:
        """Extract from LinkedIn public pages (limited without API)"""
        results = []
        # LinkedIn requires authentication for most data
        # This is a placeholder - would need LinkedIn API or scraping (terms of service apply)
        print(f"  Note: LinkedIn extraction requires API access or manual collection")
        return results
    
    def extract_from_company_website(self, domain: str) -> List[Dict]:
        """Extract influencer data from company website"""
        print(f"\nExtracting from: {domain}")
        all_results = []
        
        # Method 1: Contact/About pages
        contact_results = self.extract_from_contact_page(domain)
        all_results.extend(contact_results)
        
        # Method 2: Look for author pages (common on media sites)
        author_urls = [
            f"https://{domain}/authors",
            f"https://{domain}/writers",
            f"https://{domain}/contributors",
            f"https://www.{domain}/authors",
        ]
        
        for url in author_urls:
            print(f"  Checking authors page: {url}")
            soup = self._get_page(url)
            if soup:
                # Look for author links
                links = soup.find_all('a', href=re.compile(r'author|writer|contributor', re.I))
                print(f"    Found {len(links)} author links")
                
                for link in links[:50]:  # Increased limit
                    href = link.get('href', '')
                    if not href:
                        continue
                    
                    author_url = urljoin(url, href)
                    
                    # Try to extract name from link text first
                    name = link.get_text().strip()
                    
                    # If no name in link, try to get from URL
                    if not name or len(name) < 3:
                        # Extract from URL like /author/john-doe/
                        url_match = re.search(r'/(?:author|writer|contributor)/([^/]+)', author_url)
                        if url_match:
                            name_part = url_match.group(1).replace('-', ' ').title()
                            name = name_part
                    
                    # Visit author page to get more info
                    author_soup = self._get_page(author_url)
                    if author_soup:
                        # Try multiple methods to extract name
                        if not name or len(name) < 3:
                            # Method 1: Look for h1 tag
                            h1 = author_soup.find('h1')
                            if h1:
                                name = h1.get_text().strip()
                            
                            # Method 2: Look for title tag
                            if not name or len(name) < 3:
                                title_tag = author_soup.find('title')
                                if title_tag:
                                    title_text = title_tag.get_text()
                                    # Extract name from title like "John Doe | TechCrunch"
                                    name_match = re.search(r'^([^|]+)', title_text)
                                    if name_match:
                                        name = name_match.group(1).strip()
                            
                            # Method 3: Look for meta tags
                            if not name or len(name) < 3:
                                meta_name = author_soup.find('meta', property='og:title')
                                if meta_name and meta_name.get('content'):
                                    name = meta_name.get('content').split('|')[0].strip()
                            
                            # Method 4: Look for author name in common class/id patterns
                            if not name or len(name) < 3:
                                for selector in ['[class*="author"]', '[class*="name"]', '[id*="author"]']:
                                    elem = author_soup.select_one(selector)
                                    if elem:
                                        text = elem.get_text().strip()
                                        if len(text) > 3 and len(text) < 100:
                                            name = text
                                            break
                        
                        # Extract emails
                        text = author_soup.get_text()
                        emails = self.extract_emails_from_text(text)
                        
                        # If no emails found, try looking in mailto links
                        if not emails:
                            mailto_links = author_soup.find_all('a', href=re.compile(r'^mailto:', re.I))
                            for mailto in mailto_links:
                                email = mailto.get('href', '').replace('mailto:', '').split('?')[0]
                                if email and '@' in email:
                                    emails.append(email)
                        
                        # Add results
                        if emails:
                            for email in emails:
                                all_results.append({
                                    'email': email,
                                    'full_name': name if name and len(name) > 2 else '',
                                    'source': author_url,
                                    'domain': domain
                                })
                        elif name and len(name) > 2:
                            # Add even without email if we have a name
                            all_results.append({
                                'email': '',
                                'full_name': name,
                                'source': author_url,
                                'domain': domain
                            })
        
        return all_results
    
    def filter_influencers(self, profiles: List[Dict]) -> List[Dict]:
        """Filter to keep only influencers"""
        influencer_keywords = [
            'influencer', 'content creator', 'creator', 'blogger', 'vlogger',
            'youtuber', 'social media', 'social media manager', 'community manager',
            'marketing', 'brand ambassador', 'ambassador', 'public relations', 'pr',
            'journalist', 'reporter', 'editor', 'writer', 'author', 'columnist',
            'podcaster', 'host', 'presenter', 'correspondent', 'analyst'
        ]
        
        filtered = []
        for profile in profiles:
            # Check if name or source suggests influencer role
            name = profile.get('full_name', '').lower()
            source = profile.get('source', '').lower()
            
            is_influencer = any(keyword in name or keyword in source for keyword in influencer_keywords)
            
            # If found on author/writer pages, likely influencer
            if 'author' in source or 'writer' in source or 'contributor' in source:
                is_influencer = True
            
            if is_influencer:
                filtered.append(profile)
        
        return filtered
    
    def search_domains(self, domains: List[str], filter_influencers_only: bool = True) -> List[Dict]:
        """Search multiple domains for influencer data"""
        all_results = []
        
        for domain in domains:
            print(f"\n{'='*60}")
            print(f"Processing domain: {domain}")
            print(f"{'='*60}")
            
            results = self.extract_from_company_website(domain)
            print(f"  Found {len(results)} contacts")
            
            if filter_influencers_only:
                influencers = self.filter_influencers(results)
                print(f"  Filtered to {len(influencers)} influencers")
                all_results.extend(influencers)
            else:
                all_results.extend(results)
        
        return all_results
    
    def enrich_with_clearbit(self, email: str) -> Optional[Dict]:
        """Enrich email using Clearbit API (free tier available)"""
        # Clearbit offers free tier: 50 lookups/month
        # This is optional - can be enabled if user has Clearbit API key
        return None
    
    def _flatten_data(self, data: List[Dict]) -> List[Dict]:
        """Flatten data for export"""
        flattened = []
        for record in data:
            flat = {
                'email': record.get('email', ''),
                'full_name': record.get('full_name', ''),
                'domain': record.get('domain', ''),
                'source_url': record.get('source', ''),
                'first_name': record.get('full_name', '').split()[0] if record.get('full_name') else '',
                'last_name': ' '.join(record.get('full_name', '').split()[1:]) if record.get('full_name') else '',
            }
            flattened.append(flat)
        return flattened
    
    def export_to_csv(self, data: List[Dict], filename: str):
        """Export to CSV"""
        if not data:
            print("No data to export")
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
            print("Error: Install gspread and google-auth for Google Sheets export")
            print("Run: pip install gspread google-auth")
            return
        
        if not data:
            print("No data to export")
            return
        
        try:
            import os
            creds_path = credentials_file or os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
            
            if not os.path.exists(creds_path):
                print(f"Error: Google credentials not found at {creds_path}")
                return
            
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(creds_path, scopes=scope)
            client = gspread.authorize(creds)
            
            try:
                spreadsheet = client.open(spreadsheet_name)
                print(f"Opened existing spreadsheet: {spreadsheet_name}")
            except gspread.SpreadsheetNotFound:
                spreadsheet = client.create(spreadsheet_name)
                print(f"Created new spreadsheet: {spreadsheet_name}")
            
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
                worksheet.clear()
            except:
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=25)
            
            flattened = self._flatten_data(data)
            headers = list(flattened[0].keys())
            rows = [headers]
            
            for record in flattened:
                row = [record.get(header, '') for header in headers]
                rows.append(row)
            
            print(f"Writing {len(flattened)} records to Google Sheets...")
            worksheet.update(values=rows, range_name='A1')
            
            worksheet.format('A1:Z1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            print(f"\n✅ Successfully exported {len(flattened)} records to Google Sheets")
            print(f"   URL: {spreadsheet.url}")
            
        except Exception as e:
            print(f"Error exporting to Google Sheets: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Free Influencer Data Extractor - No paid APIs required!'
    )
    parser.add_argument('--domains', type=str, 
                       help='Comma-separated list of domains to search')
    parser.add_argument('--domains-file', type=str,
                       help='File containing domains (one per line)')
    parser.add_argument('--format', type=str, choices=['csv', 'gsheet', 'both'],
                       default='gsheet', help='Output format')
    parser.add_argument('--google-sheet', type=str,
                       help='Google Sheet name (for gsheet format)')
    parser.add_argument('--google-worksheet', type=str, default='Influencers',
                       help='Google Worksheet tab name')
    parser.add_argument('--output', type=str, default='influencer_data',
                       help='Output filename (for CSV)')
    parser.add_argument('--no-filter', action='store_true',
                       help='Disable influencer filtering')
    
    args = parser.parse_args()
    
    extractor = FreeInfluencerExtractor()
    
    # Get domains
    domains = []
    if args.domains:
        domains.extend([d.strip() for d in args.domains.split(',')])
    if args.domains_file:
        with open(args.domains_file, 'r') as f:
            domains.extend([line.strip() for line in f 
                          if line.strip() and not line.strip().startswith('#')])
    
    if not domains:
        print("Error: Please provide domains to search")
        print("Usage: python3 free_influencer_extractor.py --domains 'example.com,another.com'")
        return
    
    print(f"\n{'='*60}")
    print("🚀 FREE Influencer Data Extractor")
    print("   Using web scraping - No paid APIs required!")
    print(f"{'='*60}\n")
    
    # Extract data
    all_data = extractor.search_domains(
        domains,
        filter_influencers_only=not args.no_filter
    )
    
    if all_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if args.format in ['csv', 'both']:
            filename = f"{args.output}_{timestamp}.csv"
            extractor.export_to_csv(all_data, filename)
        
        if args.format in ['gsheet', 'both']:
            sheet_name = args.google_sheet or 'Influencer Data'
            extractor.export_to_google_sheets(
                all_data,
                spreadsheet_name=sheet_name,
                worksheet_name=args.google_worksheet
            )
        
        print(f"\n{'='*60}")
        print(f"✅ Successfully extracted {len(all_data)} influencer profiles")
        print(f"{'='*60}\n")
    else:
        print("\n⚠️  No data found. Try different domains or check website structure.")


if __name__ == "__main__":
    main()

