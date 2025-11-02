# W20 Test Dataset - Ready to Use

## Current Status

✅ **Test dataset structure is ready**: `test_dataset_w20.json`

However, we're limited to **1 company (Whatnot)** due to Algolia API pagination limits. 

## Dataset Structure

The test dataset has this format:

```json
{
  "description": "YC W20 Test Dataset for Multi-Agent Investment Analysis System",
  "batch": "W20 (Winter 2020)",
  "companies": [
    {
      "company_name": "Whatnot",
      "description": "...",
      "website": "https://www.whatnot.com",
      "yc_url": "...",
      
      // Input for your multi-agent system
      "input_data": {
        "name": "Whatnot",
        "website": "...",
        "description": "...",
        "tags": [...]
      },
      
      // Ground truth outcomes (for testing)
      "outcome": {
        "status": "funded",
        "acquired": false,
        "further_funding": true,
        "funding_rounds": [],
        "ipo": false,
        "active": false
      }
    }
  ],
  "statistics": {...}
}
```

## How to Use

```python
import json

# Load test dataset
with open('test_dataset_w20.json', 'r') as f:
    test_data = json.load(f)

# Test your multi-agent system
for company in test_data['companies']:
    # 1. Run your system
    decision = your_multi_agent_system.analyze(company['input_data'])
    # decision = "INVEST" | "MAYBE" | "PASS"
    
    # 2. Get ground truth
    outcome = company['outcome']
    is_successful = (
        outcome['further_funding'] or 
        outcome['acquired'] or 
        outcome['status'] in ['active', 'funded']
    )
    
    # 3. Compare
    correct = (decision == "INVEST" and is_successful) or \
              (decision == "PASS" and not is_successful)
    
    print(f"{company['company_name']}: {decision} vs reality → {'✅' if correct else '❌'}")
```

## Getting More W20 Companies

The Algolia API limits us to 1000 companies. To get more W20 companies:

### Option 1: Manual Addition
1. Find W20 company list from public sources
2. Add them to `yc_w20_companies.json`
3. Run: `python research_outcomes.py --input yc_w20_companies.json --batch W20`
4. Run: `python create_test_dataset.py`

### Option 2: Use Different Batch
Try a more recent batch with better API access:
```bash
python scraper.py --batches W24 F24  # Should get more companies
python research_outcomes.py --input yc_batch_companies.json --batch W24
python create_test_dataset.py --companies yc_batch_companies.json --outcomes yc_outcomes.json
```

### Option 3: Use Crunchbase API
1. Sign up for Crunchbase API
2. Search for "Y Combinator Winter 2020" companies
3. Export and add to dataset

### Option 4: Scrape YC Website Directly
Use Playwright to scrape the YC companies page with filters:
```bash
python scraper_playwright.py --batches W20
```

## Example Test Script

See `test_multi_agent.py` for a complete example of:
- Loading test dataset
- Running your multi-agent system
- Comparing predictions to outcomes
- Calculating accuracy metrics

## Known W20 Successes (For Reference)

Some W20 companies you could manually add:
- **Whatnot** - Livestream shopping (already in dataset)
- **Brex** - Corporate cards (very successful)
- **Scale AI** - Data labeling (unicorn)
- **Instabase** - No-code platform

You can research these manually and add to the dataset.

## Next Steps

1. ✅ Dataset structure is ready
2. ⏳ Add more companies (see options above)
3. ⏳ Research outcomes for all companies
4. ✅ Test your multi-agent system against the dataset

