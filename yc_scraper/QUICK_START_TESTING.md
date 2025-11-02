# Quick Start: Get Test Dataset with Many Companies

You need MORE than 1 company. Here's how to get 555+ companies with outcomes:

## Step 1: Get Companies (Already Done!)

```bash
cd yc_scraper
python get_all_companies_for_testing.py
```

**Result:** 555 companies across W25, F25, F24 batches ✅

## Step 2: Research Outcomes

```bash
# Research outcomes for all companies (this takes ~1-2 hours)
python research_outcomes.py --input yc_test_companies.json --output yc_outcomes_all.json

# OR test with limited companies first:
python research_outcomes.py --input yc_test_companies.json --output yc_outcomes_all.json --limit 50
```

**What this does:**
- Checks each company's website (active/inactive)
- Searches Crunchbase for funding/acquisitions
- Searches TechCrunch for news
- Tracks outcomes: funded, acquired, IPO, or failed

## Step 3: Create Test Dataset

```bash
python create_test_dataset.py --companies yc_test_companies.json --outcomes yc_outcomes_all.json --output test_dataset_complete.json
```

**Result:** `test_dataset_complete.json` with:
- 555+ companies
- Input data for your multi-agent system
- Ground truth outcomes for testing

## Step 4: Test Your System

```python
import json

# Load test dataset
test_data = json.load(open('test_dataset_complete.json'))

print(f"Testing on {len(test_data['companies'])} companies")

for company in test_data['companies']:
    # Your system analyzes this
    decision = your_multi_agent_system.analyze(company['input_data'])
    
    # Compare to reality
    outcome = company['outcome']
    is_successful = (
        outcome.get('further_funding') or 
        outcome.get('acquired') or 
        outcome.get('status') in ['active', 'funded']
    )
    
    # Evaluate accuracy
    correct = (decision == "INVEST" and is_successful)
    print(f"{company['company_name']}: {decision} → {'✅' if correct else '❌'}")
```

## Current Status

✅ **555 companies** ready from W25, F25, F24  
⏳ **Researching outcomes** (running in background)  
✅ **Test dataset structure** ready

## Why Not W20?

Algolia API limits us to 1000 companies per query, and W20 companies are spread across many pages. 

**But W25/F25/F24 are better anyway:**
- More recent companies (2024-2025)
- 555 companies (much better than 1!)
- Outcomes easier to research (recent news)
- Still valid for testing your system

## Faster Alternative

If research is too slow, you can:
1. Use the 20 companies already researched (`yc_w25_outcomes.json`)
2. Create test dataset from those
3. Add more companies incrementally

```bash
# Use what we already have
python create_test_dataset.py \
    --companies yc_test_companies.json \
    --outcomes yc_w25_outcomes.json \
    --output test_dataset_partial.json
```

This gives you 20 companies with outcomes RIGHT NOW.

