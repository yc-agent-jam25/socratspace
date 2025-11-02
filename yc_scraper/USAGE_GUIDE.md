# How to Find Companies That Did NOT Get Into YC

This guide explains how to find companies that didn't get into Y Combinator batches, which you can use to test your model.

## The Problem

YC doesn't publish rejected applications, so we can't directly know which companies were rejected. However, we can use a **negative filtering approach**:

1. Find companies from other sources (TechCrunch, Crunchbase, etc.)
2. Filter out companies that ARE in YC batches
3. The remaining companies are likely non-YC companies (they either didn't apply or were rejected)

## Step-by-Step Guide

### Step 1: Get YC Companies (Baseline)

First, scrape all companies that DID get into YC batches:

```bash
cd yc_scraper
python scraper.py --batches W25 F25
```

This creates `yc_batch_companies.json` with ~445 companies (162 W25 + 283 F25).

### Step 2: Find Non-YC Companies

Now, search other sources for companies and filter out YC ones:

```bash
python find_rejected.py --yc-file yc_batch_companies.json --year 2025
```

This searches:
- **TechCrunch**: Startup funding announcements
- **Crunchbase**: Recently funded companies  
- **Product Hunt**: Recent product launches

All results are filtered to exclude YC companies.

### Step 3: Better Results with Exa Search (Recommended)

For much better results, use Exa AI search:

1. Get Exa API key from https://exa.ai (free tier available)

2. Set environment variable:
   ```bash
   export EXA_API_KEY="your_key_here"
   ```

3. Run with Exa:
   ```bash
   python find_rejected.py --yc-file yc_batch_companies.json \
       --year 2025 \
       --use-exa \
       --keywords AI SaaS fintech healthtech edtech
   ```

Exa will search for articles about startups in these categories and extract company names.

## Understanding the Results

The output file contains companies that:
- ✅ Were mentioned in startup/news sources
- ✅ Are NOT in YC batches (filtered out)
- ❓ May or may not have applied to YC

**This is not a perfect list of rejected companies**, but it's a good proxy for:
- Companies that are similar to YC companies but aren't backed by YC
- Companies that likely applied but didn't get in (assuming they match the YC profile)
- A control group for testing your model

## Tips for Better Results

### 1. Use Specific Keywords

Target the same categories as YC companies:

```bash
python find_rejected.py \
    --keywords "AI startup" "SaaS B2B" "fintech" "healthtech" \
    --use-exa
```

### 2. Focus on Recent Companies

Companies launched in 2024-2025 are most likely to have applied to W25/F25:

```bash
python find_rejected.py \
    --year 2025 \
    --keywords "seed round 2024" "seed round 2025"
```

### 3. Combine Multiple Sources

Use all sources together:

```bash
python find_rejected.py \
    --sources techcrunch crunchbase producthunt \
    --keywords AI SaaS fintech \
    --use-exa
```

### 4. Manual Verification

The automated extraction isn't perfect. You may want to:
- Manually review the company names
- Check if they match YC-stage companies (seed/pre-seed)
- Filter by funding stage if possible

## Example Output

```json
[
  {
    "name": "Acme AI",
    "source": "Exa Search",
    "url": "https://techcrunch.com/...",
    "title": "Acme AI raises $2M seed round",
    "query": "AI startup funding 2025"
  },
  {
    "name": "DataFlow",
    "source": "Crunchbase",
    "url": "https://www.crunchbase.com/...",
  }
]
```

## Testing Your Model

Use the output file to:

1. **Test rejection prediction**: Run your model on companies from `rejected_companies.json`
2. **Compare against YC companies**: Run on `yc_batch_companies.json` 
3. **Evaluate**: 
   - Does your model correctly identify why YC companies were accepted?
   - Does it predict rejection for non-YC companies?
   - What patterns differentiate accepted vs. rejected?

## Limitations

⚠️ **Important caveats**:

1. **Not all are rejected**: Some companies in `rejected_companies.json` may have never applied to YC
2. **Not all are similar**: Some may be at different stages, different markets, etc.
3. **Data quality**: Company name extraction from articles isn't perfect
4. **Time mismatch**: Some companies might have applied to different batches

Use this as a **heuristic dataset** for model testing, not as ground truth.

