#!/usr/bin/env python3
"""
Fetch ALL W20 companies by fetching all pages from Algolia.
"""

from scraper import YCBatchScraper
import json
import httpx
import urllib.parse
import time


def fetch_all_w20_companies():
    """Fetch all companies and filter for W20."""
    
    scraper = YCBatchScraper()
    
    algolia_url = f"https://{scraper.ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{scraper.ALGOLIA_INDEX}/query"
    api_key_decoded = urllib.parse.unquote(scraper.ALGOLIA_API_KEY)
    
    headers = {
        **scraper.headers,
        "X-Algolia-Application-Id": scraper.ALGOLIA_APP_ID,
        "X-Algolia-API-Key": api_key_decoded,
    }
    
    all_companies = []
    current_page = 0
    hits_per_page = 1000
    total_pages = None
    
    print("📥 Fetching ALL companies from YC database...")
    
    while True:
        payload = {
            "query": "",
            "page": current_page,
            "hitsPerPage": hits_per_page,
            "tagFilters": [["ycdc_public"]]
        }
        
        try:
            response = scraper.client.post(algolia_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            hits = data.get('hits', [])
            nb_hits = data.get('nbHits', 0)
            nb_pages = data.get('nbPages', 0)
            
            if current_page == 0:
                total_pages = nb_pages
                print(f"  📊 Total companies: {nb_hits}")
                print(f"  📄 Total pages: {nb_pages}")
            
            if not hits:
                print(f"  ⚠️  No hits on page {current_page + 1}")
                break
            
            all_companies.extend(hits)
            print(f"  ✅ Page {current_page + 1}/{nb_pages}: {len(hits)} companies (running total: {len(all_companies)})")
            
            # Check if we're done
            if current_page >= nb_pages - 1:
                print(f"  ✅ Reached last page ({nb_pages})")
                break
            
            if len(hits) < hits_per_page:
                print(f"  ✅ Last page (got {len(hits)} < {hits_per_page})")
                break
            
            current_page += 1
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"  ❌ Error on page {current_page + 1}: {e}")
            break
    
    print(f"\n📦 Fetched {len(all_companies)} total companies")
    
    # Filter for Winter 2020
    print("\n🔍 Filtering for Winter 2020 batch...")
    w20_companies = []
    
    for hit in all_companies:
        batch = hit.get('batch', '').strip()
        if batch and ('winter 2020' in batch.lower() or batch.lower() == 'w20'):
            w20_companies.append(hit)
    
    print(f"✅ Found {len(w20_companies)} W20 companies")
    
    # Deduplicate by name
    seen = set()
    unique_w20 = []
    for hit in w20_companies:
        name = hit.get('name', '').strip()
        if name and name.lower() not in seen:
            seen.add(name.lower())
            unique_w20.append(hit)
    
    print(f"✅ {len(unique_w20)} unique W20 companies after deduplication")
    
    # Format
    companies_list = []
    for hit in unique_w20:
        companies_list.append({
            'name': hit.get('name', ''),
            'batch': hit.get('batch', 'Winter 2020'),
            'url': f"https://www.ycombinator.com/companies/{hit.get('slug', '')}",
            'description': hit.get('one_liner', ''),
            'website': hit.get('website', ''),
            'tags': hit.get('tags', []),
        })
    
    # Save
    with open('yc_w20_companies.json', 'w') as f:
        json.dump({'W20': companies_list}, f, indent=2)
    
    print(f"\n💾 Saved {len(companies_list)} companies to yc_w20_companies.json")
    
    if companies_list:
        print(f"\n📋 Sample companies:")
        for i, c in enumerate(companies_list[:15], 1):
            print(f"  {i:2d}. {c['name']}")
        if len(companies_list) > 15:
            print(f"  ... and {len(companies_list) - 15} more")
    
    scraper.close()
    return companies_list


if __name__ == "__main__":
    fetch_all_w20_companies()

