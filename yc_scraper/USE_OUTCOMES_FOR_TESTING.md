# Using YC Company Outcomes for Testing Your Multi-Agent System

## Overview

You now have a tool that researches YC companies to find:
1. ✅ **Further VC funding** (Series A, B, C, etc.)
2. ✅ **Acquisitions** (acquired by company X)
3. ✅ **IPOs**
4. ✅ **Failures** (inactive/dead websites)

This creates a **ground truth dataset** to test if your multi-agent system correctly identifies successful vs. failed companies.

## Quick Start

### Step 1: Get YC Companies

```bash
cd yc_scraper

# Get companies from batches you want to test
python scraper.py --batches W25 F25 W24 F24
```

This creates `yc_batch_companies.json` with all YC companies.

### Step 2: Research Outcomes

```bash
# Research all companies (takes a while - has rate limiting)
python research_outcomes.py --input yc_batch_companies.json

# Or test with a smaller batch first
python research_outcomes.py --input yc_batch_companies.json --batch W25 --limit 10
```

This creates `yc_outcomes.json` with:
- Which companies got further funding
- Which were acquired
- Which are still active
- Which failed/died

### Step 3: Use for Testing

```python
import json

# Load outcomes (ground truth)
with open('yc_outcomes.json', 'r') as f:
    outcomes = json.load(f)

# For each company, you know:
# - Did it get further funding? (outcome['further_funding'])
# - Was it acquired? (outcome['acquired'])
# - Is it still active? (outcome['status'] == 'active')

# Run your multi-agent system
for batch_name, companies in outcomes['data'].items():
    for company_outcome in companies:
        company_name = company_outcome['company_name']
        
        # Run your system
        decision = your_multi_agent_system.analyze(company_outcome)
        # decision = "INVEST" | "MAYBE" | "PASS"
        
        # Compare to reality
        actual_outcome = company_outcome['status']  # 'acquired', 'funded', 'active', 'inactive'
        
        # Metrics:
        # - If decision == "INVEST" and actual_outcome in ['acquired', 'funded', 'active'] → CORRECT
        # - If decision == "INVEST" and actual_outcome == 'inactive' → FALSE POSITIVE
        # - If decision == "PASS" and actual_outcome in ['acquired', 'funded'] → FALSE NEGATIVE
```

## Test Metrics

### 1. Precision (Investment Accuracy)
**Of companies you say "INVEST", how many actually succeeded?**

```python
invested_companies = [c for c in companies if decision == "INVEST"]
successful = [c for c in invested_companies if c['status'] in ['acquired', 'funded', 'active']]

precision = len(successful) / len(invested_companies)
print(f"Precision: {precision:.2%}")
# Higher is better - want >70% ideally
```

### 2. Recall (Catch Rate)
**Of companies that actually succeeded, how many did you identify?**

```python
actually_successful = [c for c in companies if c['status'] in ['acquired', 'funded', 'active']]
caught = [c for c in actually_successful if decision == "INVEST"]

recall = len(caught) / len(actually_successful)
print(f"Recall: {recall:.2%}")
# Higher is better - want to catch most successful companies
```

### 3. False Positive Rate
**How many failures did you mark as "good investments"?**

```python
invested_companies = [c for c in companies if decision == "INVEST"]
failures_you_missed = [c for c in invested_companies if c['status'] == 'inactive']

false_positive_rate = len(failures_you_missed) / len(invested_companies)
print(f"False Positive Rate: {false_positive_rate:.2%}")
# Lower is better - want <20% ideally
```

### 4. Success Prediction
**Can your system distinguish successful vs. failed companies?**

```python
successful_companies = [c for c in companies if c['status'] in ['acquired', 'funded']]
failed_companies = [c for c in companies if c['status'] == 'inactive']

successful_scores = [your_system.score(c) for c in successful_companies]
failed_scores = [your_system.score(c) for c in failed_companies]

import numpy as np
print(f"Successful companies avg score: {np.mean(successful_scores):.2f}")
print(f"Failed companies avg score: {np.mean(failed_scores):.2f}")
# Successful should score higher!
```

## Example Test Script

```python
#!/usr/bin/env python3
"""
Test your multi-agent system against YC outcomes.
"""

import json
from your_multi_agent_system import analyze_company

# Load ground truth
with open('yc_outcomes.json', 'r') as f:
    outcomes_data = json.load(f)

all_companies = []
for batch, companies in outcomes_data['data'].items():
    all_companies.extend(companies)

print(f"Testing on {len(all_companies)} companies...")

# Run predictions
results = []
for company in all_companies:
    # Your system analyzes the company
    decision = analyze_company(company)
    
    # Ground truth
    actual_status = company['status']
    actually_successful = actual_status in ['acquired', 'funded', 'active', 'ipo']
    
    results.append({
        'company': company['company_name'],
        'predicted': decision,
        'actual': actual_status,
        'correct': (decision == "INVEST" and actually_successful) or 
                  (decision == "PASS" and not actually_successful)
    })

# Calculate metrics
total = len(results)
correct = sum(1 for r in results if r['correct'])
accuracy = correct / total

invest_predictions = [r for r in results if r['predicted'] == "INVEST"]
invest_correct = sum(1 for r in invest_predictions if r['actual'] in ['acquired', 'funded', 'active'])
precision = invest_correct / len(invest_predictions) if invest_predictions else 0

print(f"\n📊 Results:")
print(f"   Total accuracy: {accuracy:.2%}")
print(f"   Precision (invest predictions): {precision:.2%}")
print(f"   Invested in {len(invest_predictions)} companies")
```

## Limitations & Improvements

**Current limitations:**
- Web scraping is slow and unreliable
- Some outcomes may be missed
- Need manual verification for important cases

**To improve:**
1. **Use Crunchbase API** (better data, faster)
2. **Add news search** (Google News API, Exa search)
3. **Check LinkedIn** (employee count changes indicate growth)
4. **Manual verification** for top companies

## Next Steps

1. **Run on historical batches** (W20, F20, etc.) - they have more known outcomes
2. **Compare to benchmark**: How does your system compare to YC's actual decisions?
3. **Identify patterns**: What do successful companies have in common?
4. **Iterate**: Use findings to improve your multi-agent system

