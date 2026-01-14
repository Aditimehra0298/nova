#!/usr/bin/env python3
"""
Recover and re-extract all influencer data
Extracts from all platforms and accumulates data properly
"""

import requests
import time
from datetime import datetime

API_KEY = "5c1e38a60d83acdffe5640bd3d17de2980861376"

# All domains to extract from
ALL_DOMAINS = [
    # Tech Media
    "techcrunch.com", "theverge.com", "wired.com", "arstechnica.com",
    "engadget.com", "gizmodo.com", "mashable.com", "venturebeat.com",
    "recode.net", "techradar.com", "zdnet.com", "cnet.com",
    
    # Business Media
    "forbes.com", "bloomberg.com", "wsj.com", "ft.com",
    "businessinsider.com", "cnbc.com", "reuters.com", "economist.com",
    "fortune.com", "fastcompany.com", "inc.com", "entrepreneur.com",
    
    # Marketing
    "hubspot.com", "marketingland.com", "adweek.com", "adage.com",
    "socialmediaexaminer.com", "contentmarketinginstitute.com",
    "marketo.com", "salesforce.com",
    
    # News & Media
    "cnn.com", "bbc.com", "nytimes.com", "washingtonpost.com",
    "theguardian.com", "usatoday.com", "nbcnews.com",
]

def extract_domain_batch(domains_batch):
    """Extract from a batch of domains"""
    domains_str = ",".join(domains_batch)
    
    cmd = [
        "python3", "hunter_extractor.py",
        "--api-key", API_KEY,
        "--domains", domains_str,
        "--format", "gsheet",
        "--google-sheet", "Influencer Data",
        "--limit", "10"
    ]
    
    import subprocess
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return result.returncode == 0
    except:
        return False

def main():
    print("\n" + "="*70)
    print("🔄 RECOVERING ALL INFLUENCER DATA")
    print("   Re-extracting from all platforms")
    print("="*70 + "\n")
    
    # Process in small batches to avoid rate limits
    batch_size = 3
    total_domains = len(ALL_DOMAINS)
    processed = 0
    
    for i in range(0, total_domains, batch_size):
        batch = ALL_DOMAINS[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_domains + batch_size - 1) // batch_size
        
        print(f"\n📦 Batch {batch_num}/{total_batches}: {', '.join(batch)}")
        print(f"   Progress: {processed}/{total_domains} domains")
        
        success = extract_domain_batch(batch)
        
        if success:
            print(f"   ✅ Batch {batch_num} completed")
            processed += len(batch)
        else:
            print(f"   ⚠️  Batch {batch_num} had errors (may be rate limited)")
        
        # Wait between batches
        if i + batch_size < total_domains:
            wait_time = 60  # Wait 60 seconds between batches
            print(f"   ⏳ Waiting {wait_time} seconds before next batch...")
            time.sleep(wait_time)
    
    print("\n" + "="*70)
    print("✅ RECOVERY COMPLETE!")
    print("="*70)
    print(f"\n📊 Processed {processed} domains")
    print("📝 Check your Google Sheet for all accumulated data")
    print("🔗 https://docs.google.com/spreadsheets/d/1DaplVZtlFgioBjBolJYI1A-MY_Yq8yWAVgXUqwsClK8\n")

if __name__ == "__main__":
    main()


