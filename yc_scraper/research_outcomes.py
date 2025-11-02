#!/usr/bin/env python3
"""
Research outcomes for YC companies to create test dataset.

For each YC company, finds:
1. Further VC funding (Series A, B, C, etc.)
2. Acquisitions (acquired by company X)
3. IPOs
4. Current status (active, inactive, dead)
5. Last known status date

This creates a ground truth dataset for testing your multi-agent system.
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


class CompanyOutcomeTracker:
    """Tracks outcomes for YC companies."""
    
    def __init__(self):
        """Initialize tracker."""
        self.client = httpx.Client(timeout=30, follow_redirects=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/json",
        }
        
        # Cache for API calls
        self.outcome_cache = {}
    
    def check_company_website(self, url: str) -> Dict[str, any]:
        """Check if company website is still active."""
        if not url or not url.startswith('http'):
            return {'status': 'unknown', 'active': None}
        
        try:
            response = self.client.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return {'status': 'active', 'active': True, 'http_status': 200}
            elif response.status_code in [301, 302]:
                return {'status': 'redirected', 'active': True, 'http_status': response.status_code}
            else:
                return {'status': 'inactive', 'active': False, 'http_status': response.status_code}
        except:
            return {'status': 'dead', 'active': False, 'error': 'connection_failed'}
    
    def search_crunchbase(self, company_name: str) -> Dict[str, any]:
        """Search Crunchbase for company funding/acquisition data."""
        # Note: This uses web scraping. For better results, use Crunchbase API.
        
        outcome = {
            'funding_rounds': [],
            'total_funding': None,
            'last_funding_date': None,
            'last_funding_round': None,
            'acquired_by': None,
            'acquisition_date': None,
            'ipo': False,
            'ipo_date': None,
        }
        
        try:
            # Crunchbase search URL - try multiple formats
            company_slug = company_name.lower().replace(' ', '-').replace('&', 'and')
            search_urls = [
                f"https://www.crunchbase.com/organization/{company_slug}",
                f"https://www.crunchbase.com/discover/organization.companies/{company_slug}",
            ]
            
            for search_url in search_urls:
                try:
                    response = self.client.get(search_url, headers=self.headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text = soup.get_text()
                        text_lower = text.lower()
                        
                        # Look for acquisition info
                        if 'acquired' in text_lower or 'acquisition' in text_lower:
                            # Try multiple patterns
                            patterns = [
                                r'acquired by ([A-Z][a-zA-Z0-9\s&]+)',
                                r'acquisition by ([A-Z][a-zA-Z0-9\s&]+)',
                                r'was acquired by ([A-Z][a-zA-Z0-9\s&]+)',
                            ]
                            for pattern in patterns:
                                match = re.search(pattern, text)
                                if match:
                                    outcome['acquired_by'] = match.group(1).strip()
                                    break
                        
                        # Look for IPO info
                        if any(term in text_lower for term in ['ipo', 'went public', 'public offering', 'listed on']):
                            outcome['ipo'] = True
                        
                        # Look for funding rounds (Series A, B, C, etc.)
                        funding_patterns = [
                            r'series ([ABC])',
                            r'raised.*?\$([\d.]+[MB])',
                            r'funding.*?\$([\d.]+[MB])',
                        ]
                        for pattern in funding_patterns:
                            matches = re.findall(pattern, text_lower)
                            if matches:
                                outcome['funding_rounds'] = matches
                                outcome['last_funding_round'] = matches[-1] if matches else None
                        
                        # If we found anything, break
                        if outcome['acquired_by'] or outcome['ipo'] or outcome['funding_rounds']:
                            break
                
                except Exception:
                    continue
        
        except Exception as e:
            pass  # Crunchbase scraping is unreliable, will use other methods
        
        return outcome
    
    def search_techcrunch(self, company_name: str) -> Dict[str, any]:
        """Search TechCrunch for company news."""
        outcome = {
            'techcrunch_articles': [],
            'funding_mentioned': False,
            'acquisition_mentioned': False,
        }
        
        try:
            # TechCrunch search
            search_url = f"https://techcrunch.com/search/{company_name.replace(' ', '%20')}"
            response = self.client.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text_lower = soup.get_text().lower()
                
                # Look for funding/acquisition keywords
                if any(term in text_lower for term in ['raises', 'funding', 'series', 'invests']):
                    outcome['funding_mentioned'] = True
                
                if any(term in text_lower for term in ['acquired', 'acquisition', 'bought']):
                    outcome['acquisition_mentioned'] = True
        
        except:
            pass
        
        return outcome
    
    def check_linkedin(self, company_name: str) -> Dict[str, any]:
        """Check LinkedIn for company status."""
        # LinkedIn company pages often show employee count, which indicates activity
        # But requires API or scraping LinkedIn
        
        return {'status': 'unknown'}
    
    def research_company_outcome(self, company: Dict[str, str]) -> Dict[str, any]:
        """
        Research a single company's outcome.
        
        Args:
            company: Dict with 'name', 'url', 'website', etc.
        
        Returns:
            Dict with outcome information
        """
        company_name = company.get('name', '')
        company_url = company.get('url', '')
        website = company.get('website', '') or company_url
        
        print(f"  🔍 Researching: {company_name}")
        
        outcome = {
            'company_name': company_name,
            'yc_batch': company.get('batch', ''),
            'yc_url': company_url,
            'website': website,
            'website_status': None,
            'further_funding': False,
            'funding_rounds': [],
            'acquired': False,
            'acquired_by': None,
            'acquired_date': None,
            'ipo': False,
            'status': 'unknown',  # active, acquired, failed, inactive
            'last_known_date': None,
            'sources': [],
        }
        
        # Check website status
        if website:
            website_status = self.check_company_website(website)
            outcome['website_status'] = website_status
            outcome['active'] = website_status.get('active', None)
        
        # Search Crunchbase (limited without API)
        crunchbase_data = self.search_crunchbase(company_name)
        if crunchbase_data.get('acquired_by'):
            outcome['acquired'] = True
            outcome['acquired_by'] = crunchbase_data['acquired_by']
            outcome['status'] = 'acquired'
            outcome['sources'].append('crunchbase')
        
        if crunchbase_data.get('ipo'):
            outcome['ipo'] = True
            outcome['status'] = 'ipo'
            outcome['sources'].append('crunchbase')
        
        if crunchbase_data.get('funding_rounds'):
            outcome['further_funding'] = True
            outcome['funding_rounds'] = crunchbase_data['funding_rounds']
            if outcome['status'] == 'unknown':
                outcome['status'] = 'funded'
            outcome['sources'].append('crunchbase')
        
        # Also check TechCrunch
        techcrunch_data = self.search_techcrunch(company_name)
        if techcrunch_data.get('acquisition_mentioned'):
            if not outcome['acquired']:
                outcome['acquired'] = True
                outcome['status'] = 'acquired'
            outcome['sources'].append('techcrunch')
        
        if techcrunch_data.get('funding_mentioned'):
            if not outcome['further_funding']:
                outcome['further_funding'] = True
                if outcome['status'] == 'unknown':
                    outcome['status'] = 'funded'
            outcome['sources'].append('techcrunch')
        
        # Infer status from website
        if outcome['status'] == 'unknown':
            if outcome.get('active') is False:
                outcome['status'] = 'inactive'
            elif outcome.get('active') is True:
                outcome['status'] = 'active'
        
        print(f"     Status: {outcome['status']}")
        if outcome['acquired']:
            print(f"     Acquired by: {outcome['acquired_by']}")
        if outcome['further_funding']:
            print(f"     Further funding: Yes")
        
        return outcome
    
    def research_batch(self, companies: List[Dict[str, str]], batch_name: str) -> List[Dict[str, any]]:
        """Research outcomes for a batch of companies."""
        print(f"\n📊 Researching outcomes for batch {batch_name} ({len(companies)} companies)...")
        
        outcomes = []
        
        for i, company in enumerate(companies, 1):
            try:
                outcome = self.research_company_outcome(company)
                outcomes.append(outcome)
                
                # Rate limiting
                if i % 10 == 0:
                    print(f"  ⏸️  Processed {i}/{len(companies)}, pausing...")
                    time.sleep(2)
                else:
                    time.sleep(0.5)
            
            except Exception as e:
                print(f"  ⚠️  Error researching {company.get('name', 'unknown')}: {e}")
                outcomes.append({
                    'company_name': company.get('name', ''),
                    'status': 'error',
                    'error': str(e),
                })
        
        return outcomes
    
    def save_outcomes(self, outcomes_by_batch: Dict[str, List], output_file: str = "yc_outcomes.json"):
        """Save researched outcomes."""
        
        # Calculate summary stats
        total_companies = sum(len(outcomes) for outcomes in outcomes_by_batch.values())
        
        status_counts = {}
        acquired_count = 0
        funded_count = 0
        ipo_count = 0
        
        for outcomes in outcomes_by_batch.values():
            for outcome in outcomes:
                status = outcome.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
                
                if outcome.get('acquired'):
                    acquired_count += 1
                if outcome.get('further_funding'):
                    funded_count += 1
                if outcome.get('ipo'):
                    ipo_count += 1
        
        summary = {
            'description': 'YC Company Outcomes - Ground Truth Dataset for Testing',
            'total_companies': total_companies,
            'batches': len(outcomes_by_batch),
            'summary': {
                'acquired': acquired_count,
                'further_funding': funded_count,
                'ipo': ipo_count,
                'status_breakdown': status_counts,
            },
            'data': outcomes_by_batch,
            'generated_at': datetime.now().isoformat(),
        }
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 Saved outcomes to {output_file}")
        print(f"\n📊 Summary:")
        print(f"   Total companies: {total_companies}")
        print(f"   Acquired: {acquired_count}")
        print(f"   Further funding: {funded_count}")
        print(f"   IPO: {ipo_count}")
        print(f"   Status breakdown: {status_counts}")
    
    def close(self):
        """Close HTTP client."""
        self.client.close()


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Research outcomes for YC companies (funding, acquisitions, failures)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Research outcomes for all companies in yc_batch_companies.json
  python research_outcomes.py --input yc_batch_companies.json
  
  # Research specific batch only
  python research_outcomes.py --input yc_batch_companies.json --batch W25
        """
    )
    
    parser.add_argument('--input', type=str, default='yc_batch_companies.json',
                       help='Input file with YC companies')
    parser.add_argument('--batch', type=str, default=None,
                       help='Specific batch to research (e.g., W25). If not specified, researches all.')
    parser.add_argument('--output', type=str, default='yc_outcomes.json',
                       help='Output file (default: yc_outcomes.json)')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of companies per batch (for testing)')
    
    args = parser.parse_args()
    
    # Load YC companies
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ File not found: {args.input}")
        print("   Run: python scraper.py --batches W25 F25 first")
        return
    
    with open(input_path, 'r') as f:
        yc_data = json.load(f)
    
    tracker = CompanyOutcomeTracker()
    
    try:
        outcomes_by_batch = {}
        
        # Filter by batch if specified
        batches_to_research = [args.batch] if args.batch else yc_data.keys()
        
        for batch_name in batches_to_research:
            if batch_name not in yc_data:
                print(f"⚠️  Batch {batch_name} not found in {args.input}")
                continue
            
            companies = yc_data[batch_name]
            if args.limit:
                companies = companies[:args.limit]
            
            outcomes = tracker.research_batch(companies, batch_name)
            outcomes_by_batch[batch_name] = outcomes
        
        # Save results
        tracker.save_outcomes(outcomes_by_batch, args.output)
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("\n1. Review yc_outcomes.json for accuracy")
        print("2. Manually verify important companies")
        print("3. Use this as ground truth to test your multi-agent system:")
        print("   - Run system on companies")
        print("   - Compare predictions to actual outcomes")
        print("   - Calculate accuracy metrics")
        print()
        
    finally:
        tracker.close()


if __name__ == "__main__":
    main()

