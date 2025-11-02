# Public Datasets for Testing Multi-Agent Investment Analysis

Since finding "rejected YC companies" is unreliable, here are better publicly available datasets to test your multi-agent system's efficacy.

## Option 1: Historical YC Batches (Best for Your Use Case)

**Why this works:**
- You already have W25/F25 companies (ground truth: they got in)
- Historical batches (W20, F20, etc.) have known outcomes
- You can test: "Would your system predict W20 companies correctly?"

**How to get it:**
```bash
# Scrape older batches that have known outcomes
python scraper.py --batches W20 F20 W21 F21 W22 F22 W23 F23
```

**Test approach:**
1. Get historical batch companies (e.g., W20)
2. Run your multi-agent system on them
3. Check if your system correctly identifies them as "good investments"
4. Compare success metrics: which W20 companies actually succeeded vs. your predictions

## Option 2: Crunchbase Open Data Map (Recommended)

**What it is:**
- Public dataset of companies, funding rounds, exits
- Updated monthly
- Includes success/failure indicators

**How to get:**
1. Sign up at https://data.crunchbase.com/docs/open-data-map
2. Download company dataset
3. Filter for seed-stage companies (similar to YC stage)
4. Use companies that:
   - Got seed funding but NOT from YC
   - Have known outcomes (acquired, IPO, failed, active)

**Test approach:**
- Companies that got seed funding = "good enough to get funded"
- Companies that got acquired/IPO = "success"
- Companies that failed = "failure"
- Test if your system can predict these outcomes

## Option 3: TechCrunch Crunchbase Integration

**What it is:**
- TechCrunch articles tagged with company names
- Crunchbase data embedded in articles
- Public funding announcements

**How to get:**
- Use TechCrunch API or scrape articles
- Extract company names + funding info
- Compare companies that got funding vs. didn't

**Test approach:**
- Find companies that announced seed funding in 2024
- Run your system on them BEFORE checking if they got funded
- See if your predictions match reality

## Option 4: AngelList Public Data

**What it is:**
- Public startup listings
- Funding status
- Many non-YC companies

**How to get:**
- Scrape AngelList public pages
- Extract company data
- Many companies list publicly

**Test approach:**
- Get companies that raised seed rounds (not YC)
- Compare to YC companies at similar stage
- Test if your system distinguishes them

## Option 5: Product Hunt Top Products

**What it is:**
- Products that launched on Product Hunt
- Public voting/engagement data
- Many successful non-YC startups

**How to get:**
- Product Hunt API (if available) or scrape
- Top products each day/week
- Track which became successful companies

**Test approach:**
- Products that got high Product Hunt votes
- See if your system predicts their success
- Compare to actual outcomes

## Option 6: Failed Startups Database

**What it is:**
- Public databases of failed startups
- Companies that shut down
- Known "bad" examples for testing

**How to get:**
- Failed Startup database (some exist)
- Autopsy.io, CB Insights failure lists
- Companies that publicly announced shutdowns

**Test approach:**
- Run your system on known failures
- See if it correctly identifies red flags
- Compare predictions to actual outcomes

## Recommended Test Framework

### Test 1: Historical YC Batch Prediction
```python
# Test on W20 companies (you know they got in)
# See if your system predicts them as "good"
# Measure: Precision/Recall on YC companies

test_companies = get_yc_batch("W20")  # 200+ companies
predictions = run_multi_agent_system(test_companies)
accuracy = compare_to_ground_truth(predictions, known_outcomes)
```

### Test 2: Seed-Stage Company Outcome Prediction
```python
# Get companies from Crunchbase that raised seed in 2020
# Check their 2024 status (acquired? failed? still active?)
# See if your system predicted correctly

seed_companies = get_crunchbase_seed_2020()
predictions = run_multi_agent_system(seed_companies)
outcomes_2024 = get_actual_outcomes(seed_companies)
accuracy = compare_predictions_to_outcomes(predictions, outcomes_2024)
```

### Test 3: Comparison Test
```python
# Compare YC companies vs. non-YC companies at similar stage
# See if your system distinguishes them

yc_companies = get_yc_batch("W25")  # You know these got in
non_yc_companies = get_crunchbase_seed_2024()  # Similar stage, not YC

yc_scores = run_multi_agent_system(yc_companies)
non_yc_scores = run_multi_agent_system(non_yc_companies)

# YC companies should score higher (they were selected)
if mean(yc_scores) > mean(non_yc_scores):
    print("✅ System correctly identifies YC companies as better")
```

## Quick Start: Use Historical YC Batches

**Easiest option - you already have the scraper:**

```bash
cd yc_scraper

# Get historical batches (these have known outcomes now)
python scraper.py --batches W20 F20 W21 F21

# Now you have:
# - Companies that got into YC
# - You can research which succeeded vs. failed
# - Test your system on them
```

Then:
1. Research outcomes: Which W20 companies succeeded? (acquired, IPO, still active)
2. Run your multi-agent system on all W20 companies
3. Compare predictions to actual outcomes
4. Calculate accuracy metrics

## Metrics to Track

1. **Precision**: Of companies your system says "invest", how many actually succeeded?
2. **Recall**: Of companies that actually succeeded, how many did you identify?
3. **YC vs. Non-YC**: Do YC companies score higher than similar non-YC companies?
4. **False Positive Rate**: How many "bad" companies did you mark as "good"?
5. **False Negative Rate**: How many "good" companies did you miss?

## Ready-to-Use Datasets

1. **Crunchbase Open Data**: https://data.crunchbase.com/docs/open-data-map
   - Requires free account
   - Monthly updates
   - Company + funding data

2. **Kaggle Datasets**:
   - Search "startup funding" or "venture capital"
   - Several public datasets available

3. **GitHub Datasets**:
   - Search "startup dataset" or "yc companies"
   - Some researchers publish cleaned datasets

## Next Steps

Want me to:
1. Create a script to scrape historical YC batches automatically?
2. Set up Crunchbase data integration?
3. Build a test framework to evaluate your multi-agent system?
4. Create a comparison tool (YC vs. non-YC companies)?

