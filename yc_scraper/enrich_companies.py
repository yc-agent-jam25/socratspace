#!/usr/bin/env python3
"""
Enrich YC companies with:
1. Founder names/info
2. Product idea/description
3. Dates for outcomes (funding dates, acquisition dates, etc.)

This makes the test dataset comprehensive for multi-agent testing.
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup


class CompanyEnricher:
    """Enriches company data with founders, product info, and dates."""
    
    def __init__(self):
        """Initialize enricher."""
        self.client = httpx.Client(timeout=30, follow_redirects=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/json",
        }
    
    def extract_founders_from_text(self, text: str) -> List[str]:
        """Extract founder names from text using patterns."""
        founders = []
        
        # Pattern: "Founded in YYYY by Name1, Name2, and Name3"
        patterns = [
            r'Founded(?:\s+in\s+\d{4})?\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\s*,\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+))*(?:\s+and\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+))?',
            r'(?:founded|created|started)\s+(?:in\s+\d{4}\s+)?by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\s*,\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+))*(?:\s+and\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+))?\s+(?:founded|founded\s+in)',
        ]
        
        # Better pattern: "Founded in 2024 by Name1, Name2, and Name3"
        main_pattern = r'Founded(?:\s+in\s+\d{4})?\s+by\s+([^,\n]+(?:,\s*[^,\n]+)*(?:\s+and\s+[^,\n]+)?)'
        match = re.search(main_pattern, text, re.IGNORECASE)
        if match:
            founders_text = match.group(1)
            # Split by comma and "and"
            names = re.split(r',\s*|\s+and\s+', founders_text)
            for name in names:
                name = name.strip()
                # Validate it's a reasonable name (2-3 words, capitalized)
                if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}$', name):
                    founders.append(name)
        
        return founders
    
    def scrape_yc_company_page(self, yc_url: str) -> Dict[str, any]:
        """
        Scrape YC company page for founders and product info.
        
        YC pages typically have:
        - Founder names
        - Product description
        - Launch date (when they did YC)
        """
        data = {
            'founders': [],
            'product_description': '',
            'yc_launch_date': None,
        }
        
        try:
            response = self.client.get(yc_url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page_text = soup.get_text()
                
                # Extract founders from page text (usually in format "Founded by X, Y, and Z")
                founders = self.extract_founders_from_text(page_text)
                data['founders'] = founders[:5]  # Limit to 5 founders
                
                # Also check for structured founder data
                # Look for founder cards or sections (but avoid YC partner names)
                founder_elements = soup.find_all(['a', 'div', 'span'], 
                                                   class_=re.compile(r'founder|team|team-member', re.I))
                
                for elem in founder_elements:
                    text = elem.get_text(strip=True)
                    # Skip if it's clearly a YC partner (they link to /people/)
                    if elem.find('a', href=re.compile(r'/people/')):
                        continue
                    # Extract name if it looks like a person name
                    if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}$', text):
                        if text not in founders:
                            founders.append(text)
                
                data['founders'] = list(set(founders))[:5]
                
                # Get product description
                # Look for description/mission text
                desc_selectors = [
                    'div.description',
                    'div.about',
                    'div.mission',
                    'p.description',
                    'meta[name="description"]',
                ]
                
                for selector in desc_selectors:
                    if selector.startswith('meta'):
                        meta = soup.find('meta', {'name': 'description'})
                        if meta:
                            data['product_description'] = meta.get('content', '').strip()
                            break
                    else:
                        elem = soup.select_one(selector)
                        if elem:
                            text = elem.get_text(strip=True)
                            if len(text) > 50:  # Substantial description
                                data['product_description'] = text
                                break
                
                # If no description found, try getting one-liner from page
                if not data['product_description']:
                    h1 = soup.find('h1')
                    if h1:
                        data['product_description'] = h1.get_text(strip=True)
        
        except Exception as e:
            pass  # Fail silently, will try other methods
        
        return data
    
    def get_founder_info_from_website(self, website: str, company_name: str) -> Dict[str, any]:
        """Try to get founder info from company website."""
        data = {
            'founders': [],
            'product_description': '',
        }
        
        if not website or not website.startswith('http'):
            return data
        
        try:
            response = self.client.get(website, headers=self.headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for "About" or "Team" sections
                about_section = soup.find(['section', 'div'], 
                                         class_=re.compile(r'about|team|founder', re.I))
                
                if about_section:
                    text = about_section.get_text()
                    # Look for founder names (often capitalized)
                    founder_patterns = [
                        r'(?:founded|created|started) by ([A-Z][a-z]+ [A-Z][a-z]+)',
                        r'(?:founder|co-founder|CEO):\s*([A-Z][a-z]+ [A-Z][a-z]+)',
                        r'([A-Z][a-z]+ [A-Z][a-z]+), (?:founder|CEO|CTO)',
                    ]
                    
                    for pattern in founder_patterns:
                        matches = re.findall(pattern, text)
                        for match in matches:
                            if match and match not in data['founders']:
                                data['founders'].append(match)
                
                # Get product description from homepage
                meta_desc = soup.find('meta', {'name': 'description'})
                if meta_desc:
                    data['product_description'] = meta_desc.get('content', '').strip()
                
                # Also try h1 or main heading
                if not data['product_description']:
                    h1 = soup.find('h1')
                    if h1:
                        data['product_description'] = h1.get_text(strip=True)
        
        except:
            pass
        
        return data
    
    def extract_dates_from_text(self, text: str) -> Dict[str, Optional[str]]:
        """Extract dates from text (founding, funding, acquisition)."""
        dates = {
            'founding_date': None,
            'last_funding_date': None,
            'acquisition_date': None,
        }
        
        # Pattern for "Founded in YYYY"
        founding_match = re.search(r'Founded(?:\s+in)?\s+(\d{4})', text, re.IGNORECASE)
        if founding_match:
            year = founding_match.group(1)
            dates['founding_date'] = f"{year}-01-01"  # Approximate
        
        # Pattern for funding dates: "raised $X in YYYY" or "Series A in YYYY"
        funding_match = re.search(r'(?:raised|funding|Series\s+[A-Z])\s+(?:in\s+)?(\d{4})', text, re.IGNORECASE)
        if funding_match:
            year = funding_match.group(1)
            dates['last_funding_date'] = f"{year}-01-01"  # Approximate
        
        # Pattern for acquisition: "acquired in YYYY" or "sold to X in YYYY"
        acquisition_match = re.search(r'(?:acquired|sold)\s+(?:by|to)\s+[^,]+(?:in\s+)?(\d{4})', text, re.IGNORECASE)
        if acquisition_match:
            year = acquisition_match.group(1)
            dates['acquisition_date'] = f"{year}-01-01"  # Approximate
        
        return dates
    
    def search_funding_dates(self, company_name: str, outcome: Dict = None) -> Dict[str, any]:
        """Search for funding/acquisition dates from news and existing outcome data."""
        dates = {
            'last_funding_date': None,
            'acquisition_date': None,
            'founding_date': None,
            'yc_batch_date': None,  # When they did YC
        }
        
        # First, check if outcome has any date info
        if outcome:
            if outcome.get('acquired_date'):
                dates['acquisition_date'] = outcome['acquired_date']
            # Check funding_rounds for dates
            if outcome.get('funding_rounds'):
                last_round = outcome['funding_rounds'][-1] if outcome['funding_rounds'] else None
                if last_round and isinstance(last_round, dict) and last_round.get('date'):
                    dates['last_funding_date'] = last_round.get('date')
        
        try:
            # Search TechCrunch for news about company
            search_url = f"https://techcrunch.com/search/{company_name.replace(' ', '%20')}"
            response = self.client.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                
                # Extract dates from text
                text_dates = self.extract_dates_from_text(text)
                # Merge (prefer existing dates)
                for key in dates:
                    if not dates[key] and text_dates.get(key):
                        dates[key] = text_dates[key]
                
        except:
            pass
        
        return dates
    
    def get_batch_date(self, batch: str) -> Optional[str]:
        """Get approximate date for YC batch."""
        # YC batches run:
        # Winter: January-March (W20 = Winter 2020)
        # Summer/Fall: June-August (F25 = Fall 2025, S20 = Summer 2020)
        
        if not batch:
            return None
        
        batch_lower = batch.lower()
        
        # Extract year (last 2 digits: W25 -> 2025, F24 -> 2024)
        # Or full year: "Winter 2025" -> 2025
        year_match = re.search(r'(\d{2,4})', batch)
        if year_match:
            year_str = year_match.group(1)
            # Convert 2-digit to 4-digit (assuming 20xx)
            if len(year_str) == 2:
                year = int("20" + year_str)
            else:
                year = int(year_str)
        else:
            return None
        
        # Determine season
        if 'winter' in batch_lower or batch.startswith('W'):
            return f"{year}-01-15"  # Mid-January (batch starts)
        
        if 'summer' in batch_lower or 'fall' in batch_lower or batch.startswith('F') or batch.startswith('S'):
            return f"{year}-06-15"  # Mid-June (batch starts)
        
        return None
    
    def enrich_company(self, company: Dict) -> Dict:
        """Enrich a single company with all available data."""
        company_name = company.get('company_name') or company.get('name', '')
        yc_url = company.get('yc_url', '') or company.get('url', '')
        website = company.get('website', '') or (company.get('input_data', {}).get('website', ''))
        description = company.get('description', '') or company.get('input_data', {}).get('description', '')
        
        print(f"  🔍 Enriching: {company_name}")
        
        enriched = company.copy()
        
        # First, try extracting founders from existing description text
        if description:
            founders_from_desc = self.extract_founders_from_text(description)
            if founders_from_desc:
                enriched['founders'] = founders_from_desc[:5]
        
        # Get data from YC page
        if yc_url:
            yc_data = self.scrape_yc_company_page(yc_url)
            if yc_data.get('founders'):
                # Merge founders (avoid duplicates)
                existing = enriched.get('founders', [])
                new_founders = [f for f in yc_data['founders'] if f not in existing]
                enriched['founders'] = (existing + new_founders)[:5]
            if yc_data.get('product_description'):
                enriched['product_description'] = yc_data['product_description']
        
        # Get data from company website
        if website:
            website_data = self.get_founder_info_from_website(website, company_name)
            if website_data.get('founders'):
                # Merge founders
                existing = enriched.get('founders', [])
                new_founders = [f for f in website_data['founders'] if f not in existing]
                enriched['founders'] = (existing + new_founders)[:5]
            if website_data.get('product_description') and not enriched.get('product_description'):
                enriched['product_description'] = website_data['product_description']
        
        # Use existing description if no product_description found
        if not enriched.get('product_description') and description:
            enriched['product_description'] = description
        
        # Extract founders from product_description if we have one
        if enriched.get('product_description') and not enriched.get('founders'):
            founders_from_prod = self.extract_founders_from_text(enriched['product_description'])
            if founders_from_prod:
                enriched['founders'] = founders_from_prod[:5]
        
        # Search for dates (funding, acquisition, etc.)
        outcome = enriched.get('outcome', {})
        dates = self.search_funding_dates(company_name, outcome)
        
        # Also extract dates from description/product_description text
        all_text = ' '.join([
            enriched.get('product_description', ''),
            enriched.get('description', ''),
            str(outcome.get('sources', []))
        ])
        text_dates = self.extract_dates_from_text(all_text)
        
        # Merge dates (prefer outcome dates, then text dates)
        for key in dates:
            if not dates[key] and text_dates.get(key):
                dates[key] = text_dates[key]
        
        enriched.update(dates)
        
        # Add YC batch date
        batch = enriched.get('yc_batch') or enriched.get('batch', '')
        if batch:
            batch_date = self.get_batch_date(batch)
            enriched['yc_batch_date'] = batch_date
            enriched['yc_launch_date'] = batch_date  # Approximate
        
        # Ensure we have the company name in the right place
        if not enriched.get('company_name'):
            enriched['company_name'] = company_name
        
        print(f"     Founders: {len(enriched.get('founders', []))}")
        if enriched.get('founders'):
            print(f"       {', '.join(enriched['founders'][:3])}")
        print(f"     Product: {enriched.get('product_description', '')[:80]}..." if enriched.get('product_description') else "     Product: Not found")
        
        return enriched
    
    def enrich_batch(self, companies: List[Dict], batch_name: str) -> List[Dict]:
        """Enrich all companies in a batch."""
        print(f"\n📊 Enriching batch {batch_name} ({len(companies)} companies)...")
        
        enriched_companies = []
        
        for i, company in enumerate(companies, 1):
            try:
                enriched = self.enrich_company(company)
                enriched_companies.append(enriched)
                
                # Rate limiting
                if i % 10 == 0:
                    print(f"  ⏸️  Processed {i}/{len(companies)}, pausing...")
                    time.sleep(2)
                else:
                    time.sleep(0.5)
            
            except Exception as e:
                print(f"  ⚠️  Error enriching {company.get('name', 'unknown')}: {e}")
                enriched_companies.append(company)  # Keep original if enrichment fails
        
        return enriched_companies
    
    def close(self):
        """Close HTTP client."""
        self.client.close()


def enrich_company_single(enricher: CompanyEnricher, company: Dict, index: int, total: int) -> Dict:
    """Enrich a single company (for parallel processing)."""
    try:
        enriched = enricher.enrich_company(company)
        if (index + 1) % 10 == 0:
            print(f"  ✅ Processed {index + 1}/{total} companies...")
        return enriched
    except Exception as e:
        print(f"  ⚠️  Error enriching {company.get('company_name', 'unknown')}: {e}")
        return company


def enrich_test_dataset(
    test_dataset_file: str = "test_dataset_complete.json",
    output_file: str = "test_dataset_enriched.json",
    concurrent: int = 10
):
    """Enrich the complete test dataset."""
    
    # Load test dataset
    with open(test_dataset_file, 'r') as f:
        dataset = json.load(f)
    
    companies = dataset.get('companies', [])
    total = len(companies)
    
    print("="*60)
    print("Enriching Test Dataset")
    print("="*60)
    print(f"Companies to enrich: {total}")
    print(f"Concurrent requests: {concurrent}")
    print("This will take a while (rate limiting)...")
    print()
    
    if concurrent > 1:
        # Parallel processing
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        enriched_companies = [None] * total
        
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            # Create enricher instances (one per thread)
            enrichers = [CompanyEnricher() for _ in range(concurrent)]
            
            # Submit all tasks
            futures = {}
            for i, company in enumerate(companies):
                enricher_idx = i % concurrent
                future = executor.submit(enrich_company_single, enrichers[enricher_idx], company, i, total)
                futures[future] = i
            
            # Collect results
            completed = 0
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    enriched_companies[idx] = future.result()
                    completed += 1
                    if completed % 50 == 0:
                        print(f"  ⏸️  Completed {completed}/{total}, pausing briefly...")
                        time.sleep(1)
                except Exception as e:
                    print(f"  ⚠️  Error at index {idx}: {e}")
                    enriched_companies[idx] = companies[idx]
            
            # Close all enrichers
            for enricher in enrichers:
                enricher.close()
    else:
        # Sequential processing
        enricher = CompanyEnricher()
        enriched_companies = []
        
        for i, company in enumerate(companies, 1):
            try:
                enriched = enricher.enrich_company(company)
                enriched_companies.append(enriched)
                
                if i % 50 == 0:
                    print(f"  ⏸️  Processed {i}/{total}, pausing...")
                    time.sleep(3)
            
            except KeyboardInterrupt:
                print("\n⚠️  Interrupted. Saving partial results...")
                break
            except Exception as e:
                print(f"  ⚠️  Error: {e}")
                enriched_companies.append(company)
        
        enricher.close()
    
    # Update dataset
    dataset['companies'] = enriched_companies
    
    # Update statistics
    founders_count = sum(1 for c in enriched_companies if c.get('founders'))
    product_count = sum(1 for c in enriched_companies if c.get('product_description'))
    dates_count = sum(1 for c in enriched_companies if c.get('yc_batch_date'))
    
    if 'statistics' not in dataset:
        dataset['statistics'] = {}
    dataset['statistics']['with_founders'] = founders_count
    dataset['statistics']['with_product_info'] = product_count
    dataset['statistics']['with_dates'] = dates_count
    dataset['enriched_at'] = datetime.now().isoformat()
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n💾 Enriched dataset saved to {output_file}")
    print(f"\n📊 Enrichment stats:")
    print(f"   Companies with founders: {founders_count}/{total} ({100*founders_count/total:.1f}%)")
    print(f"   Companies with product info: {product_count}/{total} ({100*product_count/total:.1f}%)")
    print(f"   Companies with YC batch dates: {dates_count}/{total} ({100*dates_count/total:.1f}%)")
    
    return dataset


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enrich test dataset with founders and product info")
    parser.add_argument('--input', type=str, default='test_dataset_complete.json',
                       help='Input test dataset')
    parser.add_argument('--output', type=str, default='test_dataset_enriched.json',
                       help='Output enriched dataset')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of companies (for testing)')
    parser.add_argument('--concurrent', type=int, default=10,
                       help='Number of concurrent requests (default: 10)')
    
    args = parser.parse_args()
    
    if args.limit:
        # Load, limit, save temporarily
        with open(args.input, 'r') as f:
            dataset = json.load(f)
        dataset['companies'] = dataset['companies'][:args.limit]
        temp_file = 'temp_test_dataset.json'
        with open(temp_file, 'w') as f:
            json.dump(dataset, f)
        args.input = temp_file
    
    enrich_test_dataset(args.input, args.output, concurrent=args.concurrent)


if __name__ == "__main__":
    main()

