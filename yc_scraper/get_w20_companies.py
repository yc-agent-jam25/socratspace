#!/usr/bin/env python3
"""
Get ALL W20 (Winter 2020) companies from YC.

Fetches all pages from Algolia to ensure we get every company.
"""

from scraper import YCBatchScraper
import json
import httpx
import urllib.parse


def get_all_w20_companies():
    """Fetch all W20 companies by getting ALL companies and filtering."""
    
    scraper = YCBatchScraper()
    
    # Use Algolia directly to fetch all pages
    algolia_url = f"https://{scraper.ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{scraper.ALGOLIA_INDEX}/query"
    api_key_decoded = urllib.parse.unquote(scraper.ALGOLIA_API_KEY)
    
    algolia_headers = {
        **scraper.headers,
        "X-Algolia-Application-Id": scraper.ALGOLIA_APP_ID,
        "X-Algolia-API-Key": api_key_decoded,
    }
    
    all_companies = []
    current_page = 0
    hits_per_page = 1000
    
    print("📥 Fetching ALL companies from YC database...")
    
    while True:
        payload = {
            "query": "",
            "page": current_page,
            "hitsPerPage": hits_per_page,
            "tagFilters": [["ycdc_public"]]
        }
        
        try:
            response = scraper.client.post(algolia_url, headers=algolia_headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            hits = data.get('hits', [])
            nb_hits = data.get('nbHits', 0)
            nb_pages = data.get('nbPages', 0)
            
            if current_page == 0:
                print(f"  📊 Total companies in database: {nb_hits}")
                print(f"  📄 Total pages: {nb_pages}")
            
            if not hits:
                break
            
            all_companies.extend(hits)
            print(f"  ✅ Page {current_page + 1}/{nb_pages}: {len(hits)} companies (total: {len(all_companies)})")
            
            # Check if we're done
            if current_page >= nb_pages - 1 or len(hits) < hits_per_page:
                break
            
            current_page += 1
            
        except Exception as e:
            print(f"  ❌ Error on page {current_page + 1}: {e}")
            break
    
    print(f"\n📦 Fetched {len(all_companies)} total companies")
    
    # Filter for W20 (Winter 2020)
    print("\n🔍 Filtering for Winter 2020 batch...")
    w20_companies = []
    
    for hit in all_companies:
        batch = hit.get('batch', '').strip().lower()
        if 'winter 2020' in batch or batch == 'w20':
            w20_companies.append(hit)
    
    print(f"✅ Found {len(w20_companies)} W20 companies")
    
    # Format companies
    companies_list = []
    for hit in w20_companies:
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
        for i, c in enumerate(companies_list[:10], 1):
            print(f"  {i}. {c['name']}")
        if len(companies_list) > 10:
            print(f"  ... and {len(companies_list) - 10} more")
    
    scraper.close()
    return companies_list


if __name__ == "__main__":
    get_all_w20_companies()

