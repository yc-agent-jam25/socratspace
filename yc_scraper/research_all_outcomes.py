#!/usr/bin/env python3
"""
Research outcomes for ALL companies in batches - optimized for large datasets.

This will take a while but gives you comprehensive test data.
"""

import json
import sys
from pathlib import Path
from research_outcomes import CompanyOutcomeTracker


def research_all_batches(
    companies_file: str = "yc_test_companies.json",
    output_file: str = "yc_outcomes_all.json",
    limit_per_batch: int = None
):
    """Research outcomes for all batches."""
    
    # Load companies
    with open(companies_file, 'r') as f:
        companies_data = json.load(f)
    
    tracker = CompanyOutcomeTracker()
    
    all_outcomes = {}
    total_companies = 0
    
    print("="*60)
    print("Researching Outcomes for All Companies")
    print("="*60)
    
    for batch_name, companies in companies_data.items():
        if limit_per_batch:
            companies = companies[:limit_per_batch]
            print(f"\n📊 Processing batch {batch_name} (limited to {limit_per_batch} companies)...")
        else:
            print(f"\n📊 Processing batch {batch_name} ({len(companies)} companies)...")
        
        total_companies += len(companies)
        
        try:
            outcomes = tracker.research_batch(companies, batch_name)
            all_outcomes[batch_name] = outcomes
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user. Saving partial results...")
            break
        except Exception as e:
            print(f"❌ Error processing {batch_name}: {e}")
            continue
    
    # Save outcomes
    tracker.save_outcomes(all_outcomes, output_file)
    
    print(f"\n✅ Research complete!")
    print(f"   Total companies researched: {total_companies}")
    print(f"   Batches processed: {len(all_outcomes)}")
    
    tracker.close()
    
    return all_outcomes


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Research outcomes for all companies")
    parser.add_argument('--input', type=str, default='yc_test_companies.json',
                       help='Companies file')
    parser.add_argument('--output', type=str, default='yc_outcomes_all.json',
                       help='Output file')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit per batch (for testing)')
    
    args = parser.parse_args()
    
    print("\n⚠️  This will take a LONG time (rate limiting between requests)")
    print("   Estimated time: ~1-2 hours for 500+ companies")
    print("   You can stop anytime with Ctrl+C and resume later")
    print()
    
    research_all_batches(args.input, args.output, args.limit)

