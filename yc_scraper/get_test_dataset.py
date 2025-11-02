#!/usr/bin/env python3
"""
Get historical YC batches for testing your multi-agent system.

This is much better than trying to find "rejected" companies:
- You have ground truth (companies that got in)
- You can research outcomes (which succeeded?)
- You can test: "Does my system correctly identify these as good investments?"
"""

import json
from pathlib import Path
from scraper import YCBatchScraper


def get_historical_batches(years_back: int = 5):
    """
    Get YC batches from the past N years for testing.
    
    Args:
        years_back: How many years back to go (default: 5 = W20-F24)
    
    Returns:
        Dictionary of batch -> companies
    """
    scraper = YCBatchScraper()
    
    # Generate batch codes (W20, F20, W21, F21, etc.)
    batches = []
    for year_offset in range(years_back, 0, -1):
        year = 2025 - year_offset
        year_short = str(year)[-2:]  # "25" from 2025
        
        batches.extend([
            f"W{year_short}",  # Winter batch
            f"F{year_short}",  # Fall batch
        ])
    
    print(f"📥 Fetching {len(batches)} historical batches for testing...")
    print(f"   Batches: {', '.join(batches)}")
    
    all_companies = {}
    
    for batch in batches:
        print(f"\n🔍 Fetching {batch}...")
        companies = scraper.get_batch_companies(batch)
        if companies:
            all_companies[batch] = companies
            print(f"   ✅ Found {len(companies)} companies")
        else:
            print(f"   ⚠️  No companies found (batch might not exist yet)")
    
    scraper.close()
    
    return all_companies


def save_for_testing(companies_by_batch: dict, output_file: str = "test_dataset_historical.json"):
    """Save companies with metadata for testing."""
    
    # Add metadata
    test_data = {
        "description": "Historical YC batches for testing multi-agent investment analysis system",
        "batches": companies_by_batch,
        "total_companies": sum(len(comps) for comps in companies_by_batch.values()),
        "note": "These companies got into YC - use as ground truth 'good investments'",
    }
    
    with open(output_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"\n💾 Saved {test_data['total_companies']} companies to {output_file}")
    
    # Also create a simple list format
    all_companies_list = []
    for batch, companies in companies_by_batch.items():
        for comp in companies:
            comp['test_batch'] = batch
            all_companies_list.append(comp)
    
    simple_output = output_file.replace('.json', '_simple.json')
    with open(simple_output, 'w') as f:
        json.dump(all_companies_list, f, indent=2)
    
    print(f"💾 Also saved simple list format: {simple_output}")
    
    return test_data


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Get historical YC batches for testing your multi-agent system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get last 5 years of batches (W20-F24)
  python get_test_dataset.py
  
  # Get last 3 years only
  python get_test_dataset.py --years 3
  
  # Custom output file
  python get_test_dataset.py --output my_test_data.json
        """
    )
    
    parser.add_argument('--years', type=int, default=5,
                       help='How many years back to fetch (default: 5)')
    parser.add_argument('--output', type=str, default='test_dataset_historical.json',
                       help='Output file (default: test_dataset_historical.json)')
    
    args = parser.parse_args()
    
    print("="*60)
    print("YC Historical Batches - Test Dataset Generator")
    print("="*60)
    print("\nThis will fetch historical YC batches that you can use to:")
    print("  1. Test if your multi-agent system identifies them as 'good investments'")
    print("  2. Compare to actual outcomes (which companies succeeded?)")
    print("  3. Validate your system's predictions against ground truth")
    print()
    
    companies = get_historical_batches(args.years)
    
    if companies:
        save_for_testing(companies, args.output)
        
        print("\n" + "="*60)
        print("NEXT STEPS FOR TESTING:")
        print("="*60)
        print("\n1. Research outcomes:")
        print("   - Which companies got acquired?")
        print("   - Which companies failed?")
        print("   - Which are still active?")
        print("\n2. Run your multi-agent system on all companies")
        print("\n3. Compare predictions to actual outcomes")
        print("\n4. Calculate metrics:")
        print("   - Precision: Of 'invest' predictions, how many succeeded?")
        print("   - Recall: Of successful companies, how many did you catch?")
        print("   - Accuracy: Overall prediction correctness")
        print()
    else:
        print("\n⚠️  No companies found. Check batch codes or network connection.")


if __name__ == "__main__":
    main()

