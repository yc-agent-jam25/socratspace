"""
Find companies that did NOT get into Y Combinator batches.

Since YC doesn't publish rejected applications, this tool:
1. Searches for companies from alternative sources (TechCrunch, Product Hunt, etc.)
2. Filters out companies that ARE in YC batches
3. Returns companies that likely applied but didn't get in, or are similar but not YC-backed
"""

import json
import re
import time
from pathlib import Path
from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote

import httpx
from bs4 import BeautifulSoup


class RejectedCompanyFinder:
    """Finds companies that didn't get into YC batches."""
    
    def __init__(self, yc_companies_file: str = "yc_batch_companies.json"):
        """Initialize with list of YC companies."""
        self.client = httpx.Client(timeout=30, follow_redirects=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/json",
        }
        
        # Load YC companies to filter out
        self.yc_companies = set()
        self.yc_companies_by_name = {}
        if Path(yc_companies_file).exists():
            with open(yc_companies_file, 'r') as f:
                yc_data = json.load(f)
                for batch, companies in yc_data.items():
                    for comp in companies:
                        name_lower = comp.get('name', '').lower().strip()
                        if name_lower:
                            self.yc_companies.add(name_lower)
                            self.yc_companies_by_name[name_lower] = comp
        
        print(f"📋 Loaded {len(self.yc_companies)} YC companies to filter out")
    
    def is_yc_company(self, company_name: str) -> bool:
        """Check if a company is in YC."""
        return company_name.lower().strip() in self.yc_companies
    
    def search_techcrunch(self, batch_year: int = 2025, limit: int = 100) -> List[Dict]:
        """Search TechCrunch for startup news (likely non-YC companies)."""
        print(f"\n🔍 Searching TechCrunch for {batch_year} startups...")
        companies = []
        
        # TechCrunch startup tags/search
        # Note: This is a simplified approach - you might need to scrape their actual search
        try:
            # Try to find startup articles from around batch time
            search_urls = [
                f"https://techcrunch.com/tag/startups/",
                f"https://techcrunch.com/search/{batch_year}/",
            ]
            
            for url in search_urls:
                try:
                    response = self.client.get(url, headers=self.headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Find article links that might mention startups
                        articles = soup.find_all('a', href=re.compile(r'/\d{4}/\d{2}/\d{2}/'))
                        
                        for article in articles[:limit]:
                            title = article.get_text(strip=True)
                            # Extract potential company names from headlines
                            # This is a heuristic approach
                            if any(word in title.lower() for word in ['raises', 'funding', 'launches', 'startup']):
                                # Try to extract company name
                                # This is imperfect but a start
                                parts = title.split()
                                if 'raises' in title.lower():
                                    # "Company X raises $Y"
                                    company_name = ' '.join(parts[:parts.index('raises')])
                                elif 'launches' in title.lower():
                                    company_name = ' '.join(parts[:parts.index('launches')])
                                else:
                                    company_name = title.split()[0] if parts else None
                                
                                if company_name and not self.is_yc_company(company_name):
                                    companies.append({
                                        'name': company_name,
                                        'source': 'TechCrunch',
                                        'url': urljoin("https://techcrunch.com", article.get('href', '')),
                                        'title': title,
                                    })
                except Exception as e:
                    print(f"  ⚠️  Error searching TechCrunch: {e}")
                    continue
        
        except Exception as e:
            print(f"  ❌ TechCrunch search failed: {e}")
        
        print(f"  Found {len(companies)} potential non-YC companies from TechCrunch")
        return companies
    
    def search_crunchbase(self, batch_year: int = 2025, limit: int = 50) -> List[Dict]:
        """Search Crunchbase for recently funded companies."""
        print(f"\n🔍 Searching Crunchbase for {batch_year} companies...")
        companies = []
        
        # Crunchbase API or scraping approach
        # Note: Crunchbase has an API but requires registration
        # This is a simplified scraping approach
        try:
            # Crunchbase recently funded page
            url = f"https://www.crunchbase.com/discover/funding_rounds/funding_type/seed"
            
            response = self.client.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find company links
                company_links = soup.find_all('a', href=re.compile(r'/organization/'))
                
                for link in company_links[:limit]:
                    company_name = link.get_text(strip=True)
                    if company_name and not self.is_yc_company(company_name):
                        companies.append({
                            'name': company_name,
                            'source': 'Crunchbase',
                            'url': urljoin("https://www.crunchbase.com", link.get('href', '')),
                        })
        except Exception as e:
            print(f"  ⚠️  Crunchbase search: {e}")
        
        print(f"  Found {len(companies)} potential non-YC companies from Crunchbase")
        return companies
    
    def search_product_hunt(self, days_back: int = 90, limit: int = 100) -> List[Dict]:
        """Search Product Hunt for recent launches (likely non-YC early stage)."""
        print(f"\n🔍 Searching Product Hunt for recent launches...")
        companies = []
        
        try:
            # Product Hunt API or scraping
            # Note: Product Hunt has an API but requires auth
            url = "https://www.producthunt.com/"
            
            response = self.client.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find product/company links
                product_links = soup.find_all('a', href=re.compile(r'/(products|topics)/'))
                
                for link in product_links[:limit]:
                    product_name = link.get_text(strip=True)
                    if product_name and len(product_name) > 2 and not self.is_yc_company(product_name):
                        companies.append({
                            'name': product_name,
                            'source': 'Product Hunt',
                            'url': urljoin("https://www.producthunt.com", link.get('href', '')),
                        })
        except Exception as e:
            print(f"  ⚠️  Product Hunt search: {e}")
        
        print(f"  Found {len(companies)} potential non-YC companies from Product Hunt")
        return companies
    
    def find_by_keywords(self, keywords: List[str], batch_year: int = 2025, use_exa: bool = False) -> List[Dict]:
        """
        Find companies by searching for keywords related to YC batches.
        Companies matching these keywords but NOT in YC are likely rejected.
        
        Args:
            keywords: List of keywords to search (e.g., ['AI', 'SaaS', 'fintech'])
            batch_year: Year of the batch
            use_exa: If True, use Exa search API (requires EXA_API_KEY env var)
        """
        print(f"\n🔍 Searching for companies by keywords: {keywords}")
        companies = []
        
        # Search queries
        search_queries = []
        for kw in keywords:
            search_queries.extend([
                f"{kw} startup funding {batch_year}",
                f"{kw} startup raises seed round {batch_year}",
                f"{kw} startup launches {batch_year}",
            ])
        
        if use_exa:
            # Try to use Exa search if available
            try:
                import os
                from exa_py import Exa
                
                exa_key = os.getenv('EXA_API_KEY')
                if not exa_key:
                    print("  ⚠️  EXA_API_KEY not set, skipping Exa search")
                    print("  💡 Set EXA_API_KEY environment variable to use Exa search")
                    return self._search_with_basic_scraping(search_queries)
                
                exa_client = Exa(api_key=exa_key)
                
                for query in search_queries[:10]:  # Limit queries
                    try:
                        print(f"  🔎 Exa search: {query}")
                        results = exa_client.search(
                            query,
                            num_results=20,
                            type="company",
                            use_autoprompt=True
                        )
                        
                        for result in results.results:
                            # Extract company name from title or URL
                            title = result.title or ""
                            company_name = self._extract_company_name(title, result.url)
                            
                            if company_name and not self.is_yc_company(company_name):
                                companies.append({
                                    'name': company_name,
                                    'source': 'Exa Search',
                                    'url': result.url,
                                    'title': title,
                                    'query': query,
                                })
                    except Exception as e:
                        print(f"  ⚠️  Exa search error for '{query}': {e}")
                        continue
                
                print(f"  ✅ Found {len(companies)} companies via Exa search")
                return companies
                
            except ImportError:
                print("  ⚠️  exa_py not installed. Install with: pip install exa-py")
                return self._search_with_basic_scraping(search_queries)
        
        return self._search_with_basic_scraping(search_queries)
    
    def _search_with_basic_scraping(self, queries: List[str]) -> List[Dict]:
        """Fallback: basic web scraping for search queries."""
        print(f"  📝 Using basic scraping (consider using Exa for better results)")
        # Placeholder - would implement Google Custom Search or similar
        return []
    
    def _extract_company_name(self, title: str, url: str) -> Optional[str]:
        """Extract company name from title or URL."""
        # Simple heuristics to extract company name
        title = title.strip()
        
        # Remove common prefixes/suffixes
        patterns_to_remove = [
            r'raises.*$', r'launches.*$', r'raises.*funding.*$',
            r'startup.*$', r'company.*$', r'^the\s+', r'\s+the\s+',
        ]
        
        for pattern in patterns_to_remove:
            title = re.sub(pattern, '', title, flags=re.I)
        
        # Take first few words as company name
        words = title.split()[:3]
        company_name = ' '.join(words).strip()
        
        # Clean up
        company_name = re.sub(r'[^\w\s&]', '', company_name)
        company_name = company_name.strip()
        
        if len(company_name) < 2 or len(company_name) > 50:
            return None
        
        return company_name
    
    def find_rejected_companies(self, 
                                batch_year: int = 2025,
                                sources: List[str] = None,
                                limit_per_source: int = 50,
                                keywords: List[str] = None,
                                use_exa: bool = False) -> List[Dict]:
        """
        Find companies that likely didn't get into YC.
        
        Args:
            batch_year: Year of the batch (2025 for W25/F25)
            sources: List of sources to search ['techcrunch', 'crunchbase', 'producthunt']
            limit_per_source: Max companies per source
        """
        if sources is None:
            sources = ['techcrunch', 'crunchbase', 'producthunt']
        
        all_companies = []
        
        if 'techcrunch' in sources:
            companies = self.search_techcrunch(batch_year, limit_per_source)
            all_companies.extend(companies)
        
        if 'crunchbase' in sources:
            companies = self.search_crunchbase(batch_year, limit_per_source)
            all_companies.extend(companies)
        
        if 'producthunt' in sources:
            companies = self.search_product_hunt(limit=limit_per_source)
            all_companies.extend(companies)
        
        # Keyword-based search (recommended for better results)
        if keywords:
            keyword_companies = self.find_by_keywords(keywords, batch_year, use_exa=use_exa)
            all_companies.extend(keyword_companies)
        
        # Remove duplicates
        seen = set()
        unique_companies = []
        for comp in all_companies:
            name_lower = comp['name'].lower().strip()
            if name_lower not in seen and name_lower:
                seen.add(name_lower)
                unique_companies.append(comp)
        
        print(f"\n✅ Found {len(unique_companies)} unique companies that are NOT in YC")
        return unique_companies
    
    def save_results(self, companies: List[Dict], output_file: str = "rejected_companies.json"):
        """Save results to JSON file."""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(companies, f, indent=2)
        print(f"\n💾 Results saved to {output_path}")
    
    def close(self):
        """Close HTTP client."""
        self.client.close()


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Find companies that didn't get into YC")
    parser.add_argument('--yc-file', type=str, default='yc_batch_companies.json',
                       help='File with YC companies (to filter out)')
    parser.add_argument('--year', type=int, default=2025,
                       help='Batch year to search around')
    parser.add_argument('--sources', nargs='+', 
                       default=['techcrunch', 'crunchbase', 'producthunt'],
                       choices=['techcrunch', 'crunchbase', 'producthunt'],
                       help='Sources to search')
    parser.add_argument('--limit', type=int, default=50,
                       help='Max companies per source')
    parser.add_argument('--output', type=str, default='rejected_companies.json',
                       help='Output file')
    parser.add_argument('--keywords', nargs='+',
                       default=['AI', 'SaaS', 'fintech', 'healthtech', 'edtech'],
                       help='Keywords to search for (e.g., AI SaaS fintech)')
    parser.add_argument('--use-exa', action='store_true',
                       help='Use Exa search API (requires EXA_API_KEY env var)')
    
    args = parser.parse_args()
    
    finder = RejectedCompanyFinder(yc_companies_file=args.yc_file)
    
    try:
        companies = finder.find_rejected_companies(
            batch_year=args.year,
            sources=args.sources,
            limit_per_source=args.limit,
            keywords=args.keywords,
            use_exa=args.use_exa
        )
        
        finder.save_results(companies, args.output)
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"\nFound {len(companies)} companies that are NOT in YC batches")
        print(f"\nSample companies:")
        for comp in companies[:10]:
            print(f"  - {comp['name']} (from {comp['source']})")
        
    finally:
        finder.close()


if __name__ == "__main__":
    main()

