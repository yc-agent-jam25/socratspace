#!/usr/bin/env python3
"""
Fast parallel research of outcomes using async/threading.

This will research all 555 companies much faster.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List
import httpx
from bs4 import BeautifulSoup
import time


class FastOutcomeTracker:
    """Fast async outcome tracker."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    
    async def check_website_async(self, client: httpx.AsyncClient, url: str) -> Dict:
        """Check website status async."""
        if not url or not url.startswith('http'):
            return {'status': 'unknown', 'active': None}
        
        try:
            response = await client.get(url, headers=self.headers, timeout=10, follow_redirects=True)
            if response.status_code == 200:
                return {'status': 'active', 'active': True, 'http_status': 200}
            elif response.status_code in [301, 302]:
                return {'status': 'redirected', 'active': True, 'http_status': response.status_code}
            else:
                return {'status': 'inactive', 'active': False, 'http_status': response.status_code}
        except:
            return {'status': 'dead', 'active': False, 'error': 'connection_failed'}
    
    async def research_company_async(self, client: httpx.AsyncClient, company: Dict) -> Dict:
        """Research single company async."""
        company_name = company.get('name', '')
        website = company.get('website', '') or company.get('url', '')
        
        outcome = {
            'company_name': company_name,
            'yc_batch': company.get('batch', ''),
            'website': website,
            'status': 'unknown',
            'further_funding': False,
            'acquired': False,
            'active': None,
        }
        
        # Check website
        if website:
            website_status = await self.check_website_async(client, website)
            outcome['website_status'] = website_status
            outcome['active'] = website_status.get('active', None)
            if outcome['active'] is True:
                outcome['status'] = 'active'
            elif outcome['active'] is False:
                outcome['status'] = 'inactive'
        
        return outcome
    
    async def research_batch_async(self, companies: List[Dict], batch_name: str, max_concurrent: int = 10) -> List[Dict]:
        """Research batch with concurrency."""
        print(f"\n📊 Researching {batch_name} ({len(companies)} companies) with {max_concurrent} concurrent requests...")
        
        async with httpx.AsyncClient(timeout=30) as client:
            # Process in batches to avoid overwhelming servers
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def research_with_semaphore(company):
                async with semaphore:
                    return await self.research_company_async(client, company)
            
            # Run all research tasks
            tasks = [research_with_semaphore(company) for company in companies]
            outcomes = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions
            results = []
            for i, outcome in enumerate(outcomes):
                if isinstance(outcome, Exception):
                    print(f"  ⚠️  Error researching {companies[i].get('name', 'unknown')}: {outcome}")
                    results.append({
                        'company_name': companies[i].get('name', ''),
                        'status': 'error',
                        'error': str(outcome),
                    })
                else:
                    results.append(outcome)
        
        return results


async def research_all_companies(
    companies_file: str = "yc_test_companies.json",
    output_file: str = "yc_outcomes_fast.json",
    max_concurrent: int = 10
):
    """Research all companies."""
    
    # Load companies
    with open(companies_file, 'r') as f:
        companies_data = json.load(f)
    
    tracker = FastOutcomeTracker()
    all_outcomes = {}
    total = 0
    
    print("="*60)
    print("Fast Parallel Outcome Research")
    print("="*60)
    print(f"Using {max_concurrent} concurrent requests")
    print(f"This will be MUCH faster than sequential research")
    
    for batch_name, companies in companies_data.items():
        total += len(companies)
        outcomes = await tracker.research_batch_async(companies, batch_name, max_concurrent)
        all_outcomes[batch_name] = outcomes
        
        # Progress update
        acquired = sum(1 for o in outcomes if o.get('acquired'))
        funded = sum(1 for o in outcomes if o.get('further_funding'))
        active = sum(1 for o in outcomes if o.get('status') == 'active')
        print(f"  ✅ Batch {batch_name}: {len(outcomes)} companies")
        print(f"     Active: {active}, Funded: {funded}, Acquired: {acquired}")
    
    # Save
    summary = {
        'description': 'YC Company Outcomes - Fast Research',
        'total_companies': total,
        'batches': len(all_outcomes),
        'data': all_outcomes,
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Saved {total} companies to {output_file}")
    return all_outcomes


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fast parallel outcome research")
    parser.add_argument('--input', type=str, default='yc_test_companies.json')
    parser.add_argument('--output', type=str, default='yc_outcomes_fast.json')
    parser.add_argument('--concurrent', type=int, default=10,
                       help='Max concurrent requests (default: 10)')
    
    args = parser.parse_args()
    
    asyncio.run(research_all_companies(args.input, args.output, args.concurrent))


if __name__ == "__main__":
    main()

