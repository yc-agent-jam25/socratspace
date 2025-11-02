#!/usr/bin/env python3
"""
Select test companies for POC:
- 10 failed companies (inactive/dead)
- 10 successful companies (got VC funding after YC)
"""

import json
import random
from typing import List, Dict


def select_test_companies(
    enriched_dataset: str = "test_dataset_enriched.json",
    output_file: str = "poc_test_companies.json",
    num_failed: int = 10,
    num_successful: int = 10
):
    """Select companies for POC testing."""
    
    # Load enriched dataset
    with open(enriched_dataset, 'r') as f:
        data = json.load(f)
    
    companies = data['companies']
    
    # Separate by status
    failed = []
    active = []
    
    for company in companies:
        outcome = company.get('outcome', {})
        
        # Failed: inactive or dead website
        if outcome.get('status') == 'inactive' or not outcome.get('active', True):
            failed.append(company)
        elif outcome.get('status') == 'active' and outcome.get('active', True):
            active.append(company)
    
    print(f"📊 Found {len(failed)} failed companies")
    print(f"📊 Found {len(active)} active companies")
    
    # Select random samples
    random.seed(42)  # For reproducibility
    
    selected_failed = random.sample(failed, min(num_failed, len(failed)))
    selected_active = random.sample(active, min(num_successful, len(active)))
    
    # Create test set
    test_companies = []
    
    for company in selected_failed:
        company['label'] = 'failed'
        company['expected_outcome'] = 'failed'
        test_companies.append(company)
    
    for company in selected_active:
        company['label'] = 'successful'
        company['expected_outcome'] = 'got_funding'  # We'll verify this with research
        test_companies.append(company)
    
    # Shuffle
    random.shuffle(test_companies)
    
    # Create output
    output = {
        'description': 'POC Test Companies for Multi-Agent System',
        'generated_at': __import__('datetime').datetime.now().isoformat(),
        'companies': test_companies,
        'statistics': {
            'total': len(test_companies),
            'failed': len(selected_failed),
            'successful': len(selected_active),
        }
    }
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Selected {len(test_companies)} test companies:")
    print(f"   Failed: {len(selected_failed)}")
    print(f"   Successful: {len(selected_active)}")
    print(f"\n💾 Saved to {output_file}")
    
    # Print selection
    print("\n📋 Selected Companies:")
    for i, company in enumerate(test_companies, 1):
        label = company.get('label', 'unknown').upper()
        batch = company.get('yc_batch', 'N/A')
        date = company.get('yc_batch_date', 'N/A')
        print(f"  {i:2d}. [{label}] {company['company_name']} ({batch} - {date})")
    
    return output


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Select test companies for POC")
    parser.add_argument('--input', type=str, default='test_dataset_enriched.json',
                       help='Input enriched dataset')
    parser.add_argument('--output', type=str, default='poc_test_companies.json',
                       help='Output test companies file')
    parser.add_argument('--failed', type=int, default=10,
                       help='Number of failed companies to select')
    parser.add_argument('--successful', type=int, default=10,
                       help='Number of successful companies to select')
    
    args = parser.parse_args()
    
    select_test_companies(
        enriched_dataset=args.input,
        output_file=args.output,
        num_failed=args.failed,
        num_successful=args.successful
    )

