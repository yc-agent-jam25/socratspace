#!/usr/bin/env python3
"""
Create comprehensive test dataset for multi-agent system.

Combines:
1. YC company data (from scraper)
2. Outcome research (funding, acquisitions, failures)
3. Formats for easy testing
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def create_test_dataset(
    companies_file: str = "yc_w20_companies.json",
    outcomes_file: str = "yc_w20_outcomes.json"
) -> Dict:
    """
    Create test dataset combining company data and outcomes.
    
    Returns dataset formatted for multi-agent system testing.
    """
    
    # Load companies
    companies_path = Path(companies_file)
    if not companies_path.exists():
        raise FileNotFoundError(f"Companies file not found: {companies_file}")
    
    with open(companies_path, 'r') as f:
        companies_data = json.load(f)
    
    # Load outcomes (if exists)
    outcomes_path = Path(outcomes_file)
    outcomes_data = {}
    if outcomes_path.exists():
        with open(outcomes_path, 'r') as f:
            outcomes_data = json.load(f)
    
    # Combine data
    test_dataset = {
        "description": "YC Test Dataset for Multi-Agent Investment Analysis System",
        "batches": list(companies_data.keys()),
        "generated_at": datetime.now().isoformat(),
        "companies": [],
        "statistics": {
            "total_companies": 0,
            "with_outcomes": 0,
            "acquired": 0,
            "further_funding": 0,
            "ipo": 0,
            "active": 0,
            "inactive": 0,
        }
    }
    
    # Get companies from all batches
    all_batch_companies = []
    for batch_name, companies in companies_data.items():
        for company in companies:
            company['batch'] = batch_name
            all_batch_companies.append(company)
    
    # Get outcomes - handle multiple batches
    outcomes_by_name = {}
    if outcomes_data.get('data'):
        for batch_name, outcomes in outcomes_data['data'].items():
            for outcome in outcomes:
                name = outcome.get('company_name', '').lower()
                outcomes_by_name[name] = outcome
    
    # Combine
    for company in all_batch_companies:
        company_name = company.get('name', '')
        company_name_lower = company_name.lower()
        
        # Get outcome if available
        outcome = outcomes_by_name.get(company_name_lower, {})
        
        # Create test entry
        test_entry = {
            # Company info (input to your system)
            "company_name": company_name,
            "description": company.get('description', ''),
            "website": company.get('website', ''),
            "yc_url": company.get('url', ''),
            "yc_batch": company.get('batch', 'Winter 2020'),
            
            # Ground truth outcomes (for testing)
            "outcome": {
                "status": outcome.get('status', 'unknown'),
                "acquired": outcome.get('acquired', False),
                "acquired_by": outcome.get('acquired_by'),
                "further_funding": outcome.get('further_funding', False),
                "funding_rounds": outcome.get('funding_rounds', []),
                "ipo": outcome.get('ipo', False),
                "active": outcome.get('active'),
                "website_status": outcome.get('website_status', {}),
                "sources": outcome.get('sources', []),
            },
            
            # For your multi-agent system to analyze
            "input_data": {
                "name": company_name,
                "website": company.get('website', ''),
                "description": company.get('description', ''),
                "tags": company.get('tags', []),
            }
        }
        
        test_dataset["companies"].append(test_entry)
        
        # Update stats
        test_dataset["statistics"]["total_companies"] += 1
        if outcome:
            test_dataset["statistics"]["with_outcomes"] += 1
            if outcome.get('acquired'):
                test_dataset["statistics"]["acquired"] += 1
            if outcome.get('further_funding'):
                test_dataset["statistics"]["further_funding"] += 1
            if outcome.get('ipo'):
                test_dataset["statistics"]["ipo"] += 1
            if outcome.get('status') == 'active':
                test_dataset["statistics"]["active"] += 1
            elif outcome.get('status') == 'inactive':
                test_dataset["statistics"]["inactive"] += 1
    
    return test_dataset


def save_test_dataset(dataset: Dict, output_file: str = "test_dataset_w20.json"):
    """Save test dataset."""
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n💾 Test dataset saved to {output_file}")
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total companies: {dataset['statistics']['total_companies']}")
    print(f"   With outcomes researched: {dataset['statistics']['with_outcomes']}")
    print(f"   Acquired: {dataset['statistics']['acquired']}")
    print(f"   Further funding: {dataset['statistics']['further_funding']}")
    print(f"   IPO: {dataset['statistics']['ipo']}")
    print(f"   Active: {dataset['statistics']['active']}")
    print(f"   Inactive: {dataset['statistics']['inactive']}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create test dataset from YC companies and outcomes",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--companies', type=str, default='yc_w20_companies.json',
                       help='Companies JSON file')
    parser.add_argument('--outcomes', type=str, default='yc_w20_outcomes.json',
                       help='Outcomes JSON file')
    parser.add_argument('--output', type=str, default='test_dataset_w20.json',
                       help='Output test dataset file')
    
    args = parser.parse_args()
    
    print("="*60)
    print("Creating Test Dataset for Multi-Agent System")
    print("="*60)
    
    try:
        dataset = create_test_dataset(args.companies, args.outcomes)
        save_test_dataset(dataset, args.output)
        
        print(f"\n✅ Test dataset ready!")
        print(f"\n📋 Usage:")
        print(f"   Load: test_data = json.load(open('{args.output}'))")
        print(f"   Test: For each company in test_data['companies']:")
        print(f"     1. Run your multi-agent system on company['input_data']")
        print(f"     2. Get prediction: 'INVEST' | 'MAYBE' | 'PASS'")
        print(f"     3. Compare to ground truth: company['outcome']")
        print(f"     4. Calculate accuracy metrics")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\n💡 Run these commands first:")
        print(f"   1. python get_all_w20.py  # Get W20 companies")
        print(f"   2. python research_outcomes.py --input yc_w20_companies.json --batch W20")
        print(f"   3. python create_test_dataset.py  # This script")


if __name__ == "__main__":
    main()

