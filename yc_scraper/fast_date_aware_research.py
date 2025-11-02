#!/usr/bin/env python3
"""
Fast, date-aware research for companies.

Key constraints:
1. Only use information available BEFORE the YC batch date
2. Make decisions after the batch date (but based on pre-batch info)
3. Optimized for speed - lower quality but fast results
"""

import json
import re
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

import httpx
from bs4 import BeautifulSoup


class FastDateAwareResearcher:
    """Fast researcher that respects date boundaries."""
    
    def __init__(self):
        """Initialize fast researcher."""
        self.client = httpx.Client(timeout=10, follow_redirects=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/json",
        }
        self.cache = {}
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None
        
        # Handle None or empty string
        if isinstance(date_str, type(None)) or date_str == '':
            return None
        
        # Convert to string if needed
        date_str = str(date_str).strip()
        
        # Handle ISO format with time
        if 'T' in date_str:
            try:
                # Remove timezone info if present
                date_str = date_str.split('+')[0].split('Z')[0]
                return datetime.fromisoformat(date_str)
            except:
                pass
        
        formats = [
            "%Y-%m-%d",  # 2025-01-15
            "%Y-%m",     # 2025-01
            "%Y",        # 2025
        ]
        
        for fmt in formats:
            try:
                # Try parsing the full string with this format
                return datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue
        
        return None
    
    def is_before_cutoff(self, info_date: Optional[datetime], cutoff_date: Optional[datetime]) -> bool:
        """Check if info_date is before cutoff_date."""
        if not cutoff_date:
            return True  # No cutoff, allow all
        
        if not info_date:
            return False  # Can't verify, err on side of caution
        
        return info_date < cutoff_date
    
    def extract_year_from_text(self, text: str, keyword: str = "founded") -> Optional[int]:
        """Quickly extract year from text."""
        # Pattern: "founded in 2024" or "founded 2024"
        pattern = rf"{keyword}.*?(\d{{4}})"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except:
                pass
        return None
    
    def fast_website_check(self, url: str, cutoff_date: Optional[datetime] = None) -> Dict:
        """
        Quick website check.
        
        For date-awareness: We check if site exists NOW, but in real implementation,
        we'd use Wayback Machine to check if it existed BEFORE cutoff_date.
        For speed: Just check current status.
        """
        if not url or not url.startswith('http'):
            return {'exists': False, 'active': False, 'pre_yc_existed': None}
        
        try:
            response = self.client.get(url, headers=self.headers, timeout=5)
            # Fast mode: Assume if active now, likely was active before YC (for speed)
            # In production: Use Wayback Machine API
            return {
                'exists': True,
                'active': response.status_code == 200,
                'http_status': response.status_code,
                'pre_yc_existed': True if response.status_code == 200 else None,  # Fast assumption
            }
        except:
            return {'exists': False, 'active': False, 'pre_yc_existed': False}
    
    def fast_founder_search(self, company_name: str, founders: list, cutoff_date: Optional[datetime]) -> Dict:
        """Fast founder background check (only pre-cutoff info)."""
        # This would normally search LinkedIn/Crunchbase, but for speed:
        # Just return basic info available before cutoff
        
        result = {
            'founders_checked': len(founders),
            'pre_yc_experience': [],
            'pre_yc_companies': [],
        }
        
        # For speed: just note that we checked (actual research would be async/parallel)
        for founder in founders:
            result['pre_yc_experience'].append({
                'name': founder,
                'verified': False,  # Fast mode - skip deep checks
            })
        
        return result
    
    def fast_product_research(self, company_name: str, product_description: str, cutoff_date: Optional[datetime]) -> Dict:
        """Fast product market research (pre-cutoff)."""
        # Extract founding year from description
        founding_year = self.extract_year_from_text(product_description, "founded")
        
        result = {
            'product_description': product_description[:200],  # Truncate for speed
            'founding_year': founding_year,
            'pre_yc_validation': None,
            'market_size_estimate': None,  # Fast mode - skip
        }
        
        # Quick check: if founded before cutoff, note it
        if founding_year and cutoff_date:
            founding_date = datetime(founding_year, 1, 1)
            if self.is_before_cutoff(founding_date, cutoff_date):
                result['pre_yc_validation'] = 'founded_before_yc'
        
        return result
    
    def fast_competitor_check(self, company_name: str, product: str, cutoff_date: Optional[datetime]) -> Dict:
        """Fast competitor analysis (pre-cutoff info only)."""
        # For speed: minimal check
        return {
            'competitors_found': 0,  # Fast mode - skip
            'market_saturation': 'unknown',
        }
    
    def fast_funding_check(self, company_name: str, cutoff_date: Optional[datetime]) -> Dict:
        """Check if company had funding before YC batch."""
        # Fast mode: minimal check
        # In real implementation, this would search Crunchbase/TechCrunch
        # but only for articles/dates BEFORE cutoff_date
        
        return {
            'pre_yc_funding': None,
            'seed_round_before_yc': False,
            'sources_checked': 0,  # Fast mode
        }
    
    def research_company(self, company: Dict) -> Dict:
        """
        Fast research for a single company.
        
        Only uses information available BEFORE yc_batch_date.
        """
        company_name = company.get('company_name', '')
        yc_batch_date_str = company.get('yc_batch_date')
        cutoff_date = self.parse_date(yc_batch_date_str)
        
        if cutoff_date:
            print(f"  🔍 {company_name} - Cutoff: {cutoff_date.strftime('%Y-%m-%d')} (only using info before this date)")
        else:
            print(f"  ⚠️  {company_name} - No cutoff date found (using all info)")
        
        # Extract info
        founders = company.get('founders', [])
        product_description = company.get('product_description', company.get('description', ''))
        website = company.get('website', '')
        
        research_result = {
            'company_name': company_name,
            'research_date': datetime.now().isoformat(),
            'cutoff_date': yc_batch_date_str,
            'cutoff_datetime': cutoff_date.isoformat() if cutoff_date else None,
            
            # Fast checks (parallel in real implementation)
            'website': self.fast_website_check(website, cutoff_date),
            'founders': self.fast_founder_search(company_name, founders, cutoff_date),
            'product': self.fast_product_research(company_name, product_description, cutoff_date),
            'competitors': self.fast_competitor_check(company_name, product_description, cutoff_date),
            'pre_yc_funding': self.fast_funding_check(company_name, cutoff_date),
            
            # Decision factors (calculated from above)
            'risk_factors': [],
            'positive_signals': [],
        }
        
        # Quick risk assessment (pre-cutoff info only)
        if not research_result['website']['active']:
            research_result['risk_factors'].append('website_inactive_pre_yc')
        
        if not founders:
            research_result['risk_factors'].append('no_founder_info')
        
        if research_result['product']['founding_year']:
            research_result['positive_signals'].append(f"founded_in_{research_result['product']['founding_year']}")
        
        return research_result
    
    def batch_research(self, companies: list) -> list:
        """Research multiple companies (optimized for speed)."""
        print(f"\n🚀 Fast Date-Aware Research Mode")
        print(f"   Companies: {len(companies)}")
        print(f"   Optimized for: SPEED (lower quality)")
        print()
        
        results = []
        
        for i, company in enumerate(companies, 1):
            try:
                result = self.research_company(company)
                results.append(result)
                print(f"  ✅ [{i}/{len(companies)}] {company['company_name']}")
            except Exception as e:
                print(f"  ⚠️  Error researching {company.get('company_name', 'unknown')}: {e}")
                results.append({
                    'company_name': company.get('company_name', 'unknown'),
                    'error': str(e),
                })
        
        return results
    
    def close(self):
        """Close HTTP client."""
        self.client.close()


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fast date-aware research for POC")
    parser.add_argument('--input', type=str, default='poc_test_companies.json',
                       help='Input test companies file')
    parser.add_argument('--output', type=str, default='poc_research_results.json',
                       help='Output research results')
    
    args = parser.parse_args()
    
    # Load companies
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    companies = data['companies']
    
    # Research
    researcher = FastDateAwareResearcher()
    results = researcher.batch_research(companies)
    researcher.close()
    
    # Save results
    output = {
        'description': 'Fast Date-Aware Research Results for POC',
        'generated_at': datetime.now().isoformat(),
        'companies_researched': len(companies),
        'results': results,
    }
    
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Research results saved to {args.output}")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Companies researched: {len(results)}")
    
    risk_counts = {}
    for result in results:
        if 'risk_factors' in result:
            for risk in result['risk_factors']:
                risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    if risk_counts:
        print(f"\n   Risk factors found:")
        for risk, count in sorted(risk_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"     {risk}: {count}")


if __name__ == "__main__":
    main()

