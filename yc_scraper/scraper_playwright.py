"""
YC Batch Scraper using Playwright (for JavaScript-rendered content)

This is an alternative scraper that uses Playwright to handle JavaScript-rendered
content on YC's website. Use this if the regular scraper doesn't work due to
dynamic content loading.
"""

import json
import re
import asyncio
from pathlib import Path
from typing import List, Dict

from playwright.async_api import async_playwright, Browser, Page


class YCBatchScraperPlaywright:
    """Scrapes Y Combinator batch information using Playwright."""
    
    BASE_URL = "https://www.ycombinator.com"
    COMPANIES_URL = "https://www.ycombinator.com/companies"
    
    async def get_batch_companies(self, page: Page, batch: str) -> List[Dict[str, str]]:
        """
        Get all companies for a specific batch using Playwright.
        
        Args:
            page: Playwright page object
            batch: Batch identifier (e.g., 'W25' for Winter 2025, 'F25' for Fall 2025)
            
        Returns:
            List of company dictionaries with name, batch, and URL
        """
        companies = []
        
        try:
            print(f"Loading companies page for batch {batch}...")
            
            # Try different URL patterns
            url_patterns = [
                f"{self.COMPANIES_URL}?batch={batch}",
                f"{self.COMPANIES_URL}?filter={batch}",
                f"{self.BASE_URL}/batches/{batch}",
            ]
            
            for url in url_patterns:
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                    
                    # Wait for company listings to load
                    await page.wait_for_selector('a[href*="/companies/"]', timeout=5000)
                    
                    # Extract company links
                    company_elements = await page.query_selector_all('a[href*="/companies/"]')
                    
                    for element in company_elements:
                        href = await element.get_attribute('href')
                        if not href or not href.startswith('/companies/'):
                            continue
                        
                        # Get company name
                        company_name = await element.inner_text()
                        if not company_name or len(company_name.strip()) < 2:
                            # Try getting from image alt or other attributes
                            img = await element.query_selector('img')
                            if img:
                                company_name = await img.get_attribute('alt') or ''
                        
                        company_name = company_name.strip()
                        
                        if company_name:
                            company_url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
                            
                            # Check if batch info is nearby (in parent element or visible text)
                            parent = await element.evaluate_handle('el => el.parentElement')
                            if parent:
                                parent_text = await parent.inner_text() if hasattr(parent, 'inner_text') else ''
                                if batch in parent_text or batch in url:
                                    companies.append({
                                        'name': company_name,
                                        'batch': batch,
                                        'url': company_url
                                    })
                    
                    if companies:
                        break
                        
                except Exception as e:
                    print(f"Error with URL {url}: {e}")
                    continue
            
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
            
        except Exception as e:
            print(f"Error fetching batch {batch}: {e}")
            return []
    
    async def scrape_batches(self, batches: List[str]) -> Dict[str, List[Dict]]:
        """Scrape multiple batches."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            results = {}
            for batch in batches:
                companies = await self.get_batch_companies(page, batch)
                results[batch] = companies
                await asyncio.sleep(1)  # Be respectful
            
            await browser.close()
            return results


async def main():
    """Main function for Playwright scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape YC batches using Playwright")
    parser.add_argument('--batches', nargs='+', default=['W25', 'F25'],
                       help='Batch codes to scrape (default: W25 F25)')
    parser.add_argument('--output', type=str, default='yc_batch_companies_playwright.json',
                       help='Output file for results')
    
    args = parser.parse_args()
    
    scraper = YCBatchScraperPlaywright()
    results = await scraper.scrape_batches(args.batches)
    
    # Save results
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")
    
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


if __name__ == "__main__":
    asyncio.run(main())

