#!/usr/bin/env python3
"""
Quick test script to verify the YC scraper works.
Run this after installing dependencies to test the scraper.
"""

from scraper import YCBatchScraper

def test_scraper():
    """Test the scraper with different batch codes."""
    scraper = YCBatchScraper()
    
    # Test batches
    test_batches = ['W25', 'F25', 'W2025', 'S25']  # S25 = Spring 2025
    
    print("Testing YC Batch Scraper\n")
    print("="*60)
    
    for batch in test_batches:
        print(f"\nTesting batch: {batch}")
        print("-" * 60)
        companies = scraper.get_batch_companies(batch)
        
        if companies:
            print(f"✅ Found {len(companies)} companies")
            print(f"Sample companies:")
            for comp in companies[:3]:
                print(f"  - {comp['name']}")
        else:
            print(f"❌ No companies found for {batch}")
            print("   This could mean:")
            print("   1. The batch doesn't exist yet")
            print("   2. The batch code format is wrong")
            print("   3. YC's API structure changed")
    
    scraper.close()
    print("\n" + "="*60)
    print("Test complete!")

if __name__ == "__main__":
    test_scraper()

