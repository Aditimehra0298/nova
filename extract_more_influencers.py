#!/usr/bin/env python3
"""
Extract MORE influencers by combining Hunter.io + Free Web Scraping
Gets maximum data from multiple sources
"""

import subprocess
import sys
import time
from datetime import datetime

def run_extraction(api_key, domains_batch, batch_name):
    """Run extraction for a batch of domains"""
    print(f"\n{'='*70}")
    print(f"📊 Batch: {batch_name}")
    print(f"{'='*70}\n")
    
    domains_str = ",".join(domains_batch)
    
    # Run Hunter.io extractor
    cmd = [
        "python3", "hunter_extractor.py",
        "--api-key", api_key,
        "--domains", domains_str,
        "--format", "gsheet",
        "--google-sheet", "Influencer Data",
        "--limit", "10"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    api_key = "5c1e38a60d83acdffe5640bd3d17de2980861376"
    
    # More domains to search (organized in batches)
    all_domains = {
        "Tech Media": [
            "techcrunch.com", "theverge.com", "wired.com", "arstechnica.com",
            "engadget.com", "gizmodo.com", "mashable.com", "venturebeat.com",
            "recode.net", "techradar.com", "zdnet.com", "cnet.com"
        ],
        "Business Media": [
            "forbes.com", "bloomberg.com", "wsj.com", "ft.com",
            "businessinsider.com", "cnbc.com", "reuters.com", "economist.com",
            "fortune.com", "fastcompany.com", "inc.com", "entrepreneur.com"
        ],
        "Marketing & PR": [
            "hubspot.com", "marketingland.com", "adweek.com", "adage.com",
            "socialmediaexaminer.com", "contentmarketinginstitute.com",
            "marketo.com", "salesforce.com", "mailchimp.com"
        ],
        "Content Platforms": [
            "medium.com", "substack.com", "ghost.org", "wordpress.com",
            "tumblr.com", "blogger.com"
        ],
        "News & Media": [
            "cnn.com", "bbc.com", "nytimes.com", "washingtonpost.com",
            "theguardian.com", "usatoday.com", "nbcnews.com"
        ],
        "Tech Companies": [
            "microsoft.com", "google.com", "apple.com", "amazon.com",
            "meta.com", "twitter.com", "linkedin.com"
        ]
    }
    
    print("\n" + "="*70)
    print("🚀 EXTRACTING MORE INFLUENCERS")
    print("   Combining Hunter.io + Multiple Domain Batches")
    print("="*70)
    
    total_extracted = 0
    
    for batch_name, domains in all_domains.items():
        print(f"\n⏳ Processing {batch_name}...")
        print(f"   Domains: {len(domains)}")
        
        # Process in smaller batches to avoid rate limits
        batch_size = 3
        for i in range(0, len(domains), batch_size):
            batch = domains[i:i+batch_size]
            print(f"\n   Processing batch {i//batch_size + 1}: {', '.join(batch)}")
            
            success = run_extraction(api_key, batch, f"{batch_name} - Batch {i//batch_size + 1}")
            
            if success:
                print(f"   ✅ Batch completed")
            else:
                print(f"   ⚠️  Batch had errors (may be rate limited)")
            
            # Wait between batches to avoid rate limits
            if i + batch_size < len(domains):
                print(f"   ⏳ Waiting 30 seconds before next batch...")
                time.sleep(30)
        
        print(f"\n✅ {batch_name} completed!")
        print(f"   Waiting 60 seconds before next category...")
        time.sleep(60)
    
    print("\n" + "="*70)
    print("✅ EXTRACTION COMPLETE!")
    print("="*70)
    print("\n📊 Check your Google Sheet for all extracted influencers")
    print("🔗 https://docs.google.com/spreadsheets/d/1DaplVZtlFgioBjBolJYI1A-MY_Yq8yWAVgXUqwsClK8\n")

if __name__ == "__main__":
    main()


