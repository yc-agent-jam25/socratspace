#!/usr/bin/env python3
"""
Get ALL companies from multiple batches for testing.

Since W20 has API limitations, let's use W25/F25 (445 companies) + older batches we can get.
"""

from scraper import YCBatchScraper
import json
from pathlib import Path


def get_companies_for_testing():
    """Get companies from multiple batches for comprehensive testing."""
    
    scraper = YCBatchScraper()
    
    # Batches to try (prioritize ones we know work)
    batches_to_try = [
        'W25', 'F25',  # We know these work (445 companies)
        'W24', 'F24',  # Recent batches
        'W23', 'F23',  # 2023 batches
        'W22', 'F22',  # 2022 batches  
    ]
    
    all_companies = {}
    total = 0
    
    print("="*60)
    print("Fetching Companies for Test Dataset")
    print("="*60)
    
    for batch in batches_to_try:
        print(f"\n🔍 Fetching batch {batch}...")
        companies = scraper.get_batch_companies(batch)
        
        if companies:
            all_companies[batch] = companies
            total += len(companies)
            print(f"   ✅ Got {len(companies)} companies")
        else:
            print(f"   ⚠️  No companies found")
    
    print(f"\n📊 Summary: {total} total companies across {len(all_companies)} batches")
    
    # Save
    output_file = 'yc_test_companies.json'
    with open(output_file, 'w') as f:
        json.dump(all_companies, f, indent=2)
    
    print(f"💾 Saved to {output_file}")
    
    # Show breakdown
    print(f"\n📋 Batch breakdown:")
    for batch, companies in sorted(all_companies.items()):
        print(f"   {batch}: {len(companies)} companies")
    
    scraper.close()
    return all_companies


if __name__ == "__main__":
    companies = get_companies_for_testing()
    
    print(f"\n✅ Ready! Now run:")
    print(f"   python research_outcomes.py --input yc_test_companies.json")
    print(f"   python create_test_dataset.py --companies yc_test_companies.json --outcomes yc_outcomes.json")

