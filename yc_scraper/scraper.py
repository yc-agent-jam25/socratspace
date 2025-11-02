"""
YC Batch Rejection Scraper

This tool scrapes Y Combinator's website to find companies that did NOT get into
Winter 2025 or Fall 2025 batches. It compares the scraped data against a list
of companies that were accepted (for testing/verification).
"""

import json
import re
import time
import urllib.parse
from pathlib import Path
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup


class YCBatchScraper:
    """Scrapes Y Combinator batch information from their website."""
    
    BASE_URL = "https://www.ycombinator.com"
    COMPANIES_URL = "https://www.ycombinator.com/companies"
    
    # Algolia configuration from YC's website
    ALGOLIA_APP_ID = "45BWZJ1SGC"
    ALGOLIA_API_KEY = "MjBjYjRiMzY0NzdhZWY0NjExY2NhZjYxMGIxYjc2MTAwNWFkNTkwNTc4NjgxYjU0YzFhYTY2ZGQ5OGY5NDMxZnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMiUyQyUyMllDQ29tcGFueV9CeV9MYXVuY2hfRGF0ZV9wcm9kdWN0aW9uJTIyJTVEJnRhZ0ZpbHRlcnM9JTVCJTIyeWNkY19wdWJsaWMlMjIlNUQmYW5hbHl0aWNzVGFncz0lNUIlMjJ5Y2RjJTIyJTVE"
    ALGOLIA_INDEX = "YCCompany_production"
    
    def __init__(self, timeout: int = 30):
        """Initialize the scraper with HTTP client."""
        self.client = httpx.Client(timeout=timeout, follow_redirects=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    
    def _normalize_batch_code(self, batch: str) -> List[str]:
        """Convert batch codes like W25, F25 to YC's format like 'Winter 2025', 'Fall 2025'."""
        batch = batch.upper().strip()
        variants = []
        
        # W25, W2025 → Winter 2025
        if batch.startswith('W'):
            year = batch[1:]
            if len(year) == 2:
                year = '20' + year  # W25 → 2025
            variants.append(f"Winter {year}")
            variants.append(f"W{year[-2:]}")  # Also try W25 format
        
        # F25, S25 → Fall 2025 or Summer 2025
        elif batch.startswith('F'):
            year = batch[1:]
            if len(year) == 2:
                year = '20' + year
            variants.append(f"Fall {year}")
            variants.append(f"Summer {year}")  # YC sometimes calls fall "summer"
            variants.append(f"F{year[-2:]}")
        
        # S25 → Summer 2025
        elif batch.startswith('S'):
            year = batch[1:]
            if len(year) == 2:
                year = '20' + year
            variants.append(f"Summer {year}")
            variants.append(f"S{year[-2:]}")
        
        # Add original in case it's already in correct format
        variants.insert(0, batch)
        return list(set(variants))  # Remove duplicates
    
    def search_algolia(self, batch: str, page: int = 0, hits_per_page: int = 1000) -> Optional[List[Dict]]:
        """Search YC companies using Algolia API."""
        
        algolia_url = f"https://{self.ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{self.ALGOLIA_INDEX}/query"
        
        # Decode the URL-encoded API key from YC's HTML
        api_key_decoded = urllib.parse.unquote(self.ALGOLIA_API_KEY)
        
        # Convert batch code to YC's format (W25 → "Winter 2025")
        batch_variants = self._normalize_batch_code(batch)
        print(f"  🔄 Trying batch variants: {batch_variants}")
        
        algolia_headers = {
            **self.headers,
            "X-Algolia-Application-Id": self.ALGOLIA_APP_ID,
            "X-Algolia-API-Key": api_key_decoded,
        }
        
        # Get ALL companies (no filter), then filter in Python
        # Algolia filters don't work well with string matching
        print(f"  📥 Fetching all companies (will filter by batch in Python)...")
        
        all_results = []
        current_page = 0
        max_pages = 10  # Limit to prevent infinite loops
        
        while current_page < max_pages:
            payload = {
                "query": "",
                "page": current_page,
                "hitsPerPage": hits_per_page,
                "tagFilters": [["ycdc_public"]]
            }
            
            try:
                response = self.client.post(algolia_url, headers=algolia_headers, json=payload)
                response.raise_for_status()
                data = response.json()
                hits = data.get('hits', [])
                nb_hits = data.get('nbHits', 0)
                nb_pages = data.get('nbPages', 0)
                
                if current_page == 0:
                    print(f"  📊 Total companies in index: {nb_hits}")
                
                if not hits:
                    break
                
                all_results.extend(hits)
                
                # Check if we have more pages
                if current_page >= nb_pages - 1 or len(hits) < hits_per_page:
                    break
                
                current_page += 1
                
            except httpx.HTTPStatusError as e:
                print(f"  ❌ HTTP error ({e.response.status_code}): {e}")
                break
            except Exception as e:
                print(f"  ❌ Error fetching page {current_page}: {e}")
                break
        
        print(f"  📦 Fetched {len(all_results)} total companies")
        
        # Filter by batch in Python
        filtered_results = []
        for hit in all_results:
            hit_batch = hit.get('batch', '').strip()
            if not hit_batch:
                continue
            
            # Check if any batch variant matches
            for variant in batch_variants:
                if variant.lower() in hit_batch.lower() or hit_batch.lower() in variant.lower():
                    filtered_results.append(hit)
                    break
        
        if filtered_results:
            print(f"  ✅ Found {len(filtered_results)} companies matching batch {batch}")
            # Show sample batches to verify
            sample_batches = set([hit.get('batch', '') for hit in filtered_results[:5]])
            print(f"  📋 Sample matching batches: {sample_batches}")
            return filtered_results
        else:
            print(f"  ⚠️  No companies found matching batch variants: {batch_variants}")
            # Show what batches we actually have
            unique_batches = sorted(set([hit.get('batch', 'N/A') for hit in all_results[:100] if hit.get('batch')]))
            print(f"  📋 Available batch formats in data (sample): {unique_batches[:20]}")
            return []
    
    def get_batch_companies(self, batch: str) -> List[Dict[str, str]]:
        """
        Get all companies for a specific batch (e.g., 'W25', 'F25').
        
        Args:
            batch: Batch identifier (e.g., 'W25' for Winter 2025, 'F25' for Fall 2025)
            
        Returns:
            List of company dictionaries with name, batch, and URL
        """
        companies = []
        
        try:
            # Try Algolia API first (YC uses Algolia for search)
            print(f"\n🔍 Searching Algolia for batch {batch}...")
            hits = self.search_algolia(batch)
            
            if hits and len(hits) > 0:
                companies = []
                for hit in hits:
                    company_name = hit.get('name', '')
                    if not company_name:
                        continue
                    
                    slug = hit.get('slug', '')
                    company_url = f"{self.COMPANIES_URL}/{slug}" if slug else None
                    
                    companies.append({
                        'name': company_name,
                        'batch': hit.get('batch', batch),
                        'url': company_url,
                        'description': hit.get('one_liner', ''),
                        'website': hit.get('website', ''),
                    })
                
                if companies:
                    print(f"Found {len(companies)} companies via Algolia for batch {batch}")
                    return companies
            
            # Fallback: Try API endpoints
            api_patterns = [
                f"{self.BASE_URL}/api/companies?batch={batch}",
                f"{self.BASE_URL}/api/v1/companies?batch={batch}",
                f"{self.COMPANIES_URL}.json?batch={batch}",
            ]
            
            for api_url in api_patterns:
                try:
                    print(f"Trying API endpoint: {api_url}")
                    api_response = self.client.get(api_url, headers=self.headers)
                    if api_response.status_code == 200:
                        api_data = api_response.json()
                        if isinstance(api_data, list) and len(api_data) > 0:
                            companies = [
                                {
                                    'name': company.get('name', ''),
                                    'batch': batch,
                                    'url': company.get('url', f"{self.COMPANIES_URL}/{company.get('slug', '')}")
                                }
                                for company in api_data
                                if company.get('name')
                            ]
                            if companies:
                                print(f"Found {len(companies)} companies via API for batch {batch}")
                                return companies
                        elif isinstance(api_data, dict) and 'companies' in api_data:
                            companies = [
                                {
                                    'name': company.get('name', ''),
                                    'batch': batch,
                                    'url': company.get('url', f"{self.COMPANIES_URL}/{company.get('slug', '')}")
                                }
                                for company in api_data['companies']
                                if company.get('name')
                            ]
                            if companies:
                                print(f"Found {len(companies)} companies via API for batch {batch}")
                                return companies
                except (httpx.HTTPError, json.JSONDecodeError, KeyError):
                    continue
            
            # If Algolia didn't work, suggest using Playwright
            if not companies:
                print(f"\n⚠️  Could not find companies for batch {batch}")
                print("   This might be because:")
                print("   1. The batch code format is different (try 'W2025' or 'F2025')")
                print("   2. YC's Algolia API structure changed")
                print("   3. The batch hasn't been published yet")
                print("\n   Try using the Playwright scraper instead:")
                print("   python scraper_playwright.py --batches W25 F25")
            
            # Remove duplicates
            seen = set()
            unique_companies = []
            for comp in companies:
                comp_key = (comp['name'].lower(), comp['url'])
                if comp_key not in seen:
                    seen.add(comp_key)
                    unique_companies.append(comp)
            
            companies = unique_companies
            print(f"Found {len(companies)} companies for batch {batch}")
            return companies
            
        except httpx.HTTPError as e:
            print(f"HTTP error fetching batch {batch}: {e}")
            print("Note: YC's website may require JavaScript rendering. Consider using Playwright.")
            return []
        except Exception as e:
            print(f"Unexpected error for batch {batch}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _scrape_all_companies_for_batch(self, soup: BeautifulSoup = None, batch: str = None) -> List[Dict[str, str]]:
        """Fallback method to scrape all companies and filter by batch."""
        companies = []
        
        if soup is None:
            # Try to get the main companies page
            try:
                response = self.client.get(self.COMPANIES_URL, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                else:
                    return companies
            except httpx.HTTPError:
                return companies
        
        # Look for company listings with batch information
        # YC often displays batch info in various formats
        company_cards = soup.find_all(['div', 'li'], class_=re.compile(r'company', re.I))
        
        for card in company_cards:
            # Try to find batch indicator
            batch_indicators = card.find_all(text=re.compile(batch, re.I))
            if batch_indicators:
                link = card.find('a', href=re.compile(r'/companies/'))
                if link:
                    companies.append({
                        'name': link.get_text(strip=True) or card.get_text(strip=True),
                        'batch': batch,
                        'url': urljoin(self.BASE_URL, link.get('href', ''))
                    })
        
        return companies
    
    def search_companies_not_in_batches(self, 
                                       target_batches: List[str],
                                       accepted_companies_file: str = None) -> Dict[str, List[Dict]]:
        """
        Find companies that applied but didn't get into specified batches.
        
        This is a placeholder method since YC doesn't publicly list rejected applications.
        This tool is designed to help identify companies that may have been rejected
        by comparing against known accepted companies.
        
        Args:
            target_batches: List of batches to check (e.g., ['W25', 'F25'])
            accepted_companies_file: Path to JSON file with companies that got in
            
        Returns:
            Dictionary with batch names as keys and lists of companies as values
        """
        results = {}
        accepted_companies = set()
        
        # Load accepted companies if provided
        if accepted_companies_file and Path(accepted_companies_file).exists():
            with open(accepted_companies_file, 'r') as f:
                accepted_data = json.load(f)
                if isinstance(accepted_data, list):
                    accepted_companies = {comp.get('name', '').lower() for comp in accepted_data}
                elif isinstance(accepted_data, dict):
                    accepted_companies = {comp.get('name', '').lower() 
                                         for comp in accepted_data.get('companies', [])}
        
        # Get all companies from target batches
        all_batch_companies = set()
        for batch in target_batches:
            companies = self.get_batch_companies(batch)
            results[batch] = companies
            all_batch_companies.update({comp['name'].lower() for comp in companies})
            
            # Small delay to be respectful
            time.sleep(1)
        
        # If we have accepted companies list, show what we found
        if accepted_companies:
            print(f"\nAccepted companies loaded: {len(accepted_companies)}")
            print(f"Companies found in batches: {len(all_batch_companies)}")
            
            # Find accepted companies that are in batches (for verification)
            in_batches = accepted_companies & all_batch_companies
            print(f"Accepted companies found in batches: {len(in_batches)}")
            
            # Find accepted companies NOT in batches (might indicate error or different batch)
            not_found = accepted_companies - all_batch_companies
            if not_found:
                print(f"\nAccepted companies NOT found in scraped batches:")
                for comp in sorted(not_found):
                    print(f"  - {comp}")
        
        return results
    
    def save_results(self, results: Dict[str, List[Dict]], output_file: str = "yc_batch_companies.json"):
        """Save scraped results to JSON file."""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_path}")
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


def main():
    """Main function to run the scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape YC batches for company information")
    parser.add_argument('--batches', nargs='+', default=['W25', 'F25'],
                       help='Batch codes to scrape (default: W25 F25)')
    parser.add_argument('--accepted', type=str,
                       help='Path to JSON file with companies that got in')
    parser.add_argument('--output', type=str, default='yc_batch_companies.json',
                       help='Output file for results (default: yc_batch_companies.json)')
    
    args = parser.parse_args()
    
    scraper = YCBatchScraper()
    
    try:
        results = scraper.search_companies_not_in_batches(
            target_batches=args.batches,
            accepted_companies_file=args.accepted
        )
        
        scraper.save_results(results, args.output)
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        for batch, companies in results.items():
            print(f"\nBatch {batch}: {len(companies)} companies found")
            if companies:
                print("Sample companies:")
                for comp in companies[:5]:
                    print(f"  - {comp['name']}")
                if len(companies) > 5:
                    print(f"  ... and {len(companies) - 5} more")
    
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

