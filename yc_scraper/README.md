# YC Batch Rejection Scraper

This is a standalone web scraping tool to find companies that didn't get into Y Combinator's Winter 2025 or Fall 2025 batches. This tool is **not part of the main Socratic software** and is kept in a separate folder.

## Purpose

**For Testing Your Multi-Agent Investment Analysis System:**

The best way to test your system's efficacy is using **historical YC batches** with known outcomes, not trying to find rejected companies.

### Recommended Approach:
1. Get historical YC batches (W20, F20, etc.) - companies that got in
2. Research outcomes: Which succeeded? Which failed?
3. Run your multi-agent system on them
4. Compare predictions to actual outcomes
5. Calculate accuracy metrics

**See `test_datasets.md` for full guide on testing datasets.**

## Installation

1. Navigate to this directory:
   ```bash
   cd yc_scraper
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Test the scraper:
   ```bash
   python test_scraper.py
   ```

## Usage

### Step 1: Get YC Companies (Those That Got In)

First, scrape companies that DID get into batches:

```bash
python scraper.py --batches W25 F25
```

This creates `yc_batch_companies.json` with all companies that got in.

### Step 2: Find Companies That Did NOT Get In

### Option A: Reddit Search (Recommended - Safer Heuristic)

Reddit has first-hand accounts from founders discussing YC rejections:

```bash
python find_rejected_reddit.py --yc-file yc_batch_companies.json --year 2025
```

This searches subreddits like:
- **r/ycombinator**: Direct YC application discussions
- **r/startups**: Startup founder stories
- **r/entrepreneur**: Entrepreneur experiences

**Why this is safer:**
- Real first-hand accounts from founders
- People often mention their company name when discussing rejections
- More reliable than scraping generic startup news
- Posts often include context about why they didn't get in

### Option B: Generic Sources

```bash
python find_rejected.py --yc-file yc_batch_companies.json --year 2025
```

This searches:
- **TechCrunch**: For startup funding announcements
- **Crunchbase**: For recently funded companies  
- **Product Hunt**: For recent product launches

All companies found are filtered to exclude any that are in YC batches.

### With Accepted Companies File

If you have a list of companies that got in (for testing/verification):
```bash
python scraper.py --batches W25 F25 --accepted accepted_companies_sample.json
```

### Custom Output File

Specify a different output file:
```bash
python scraper.py --batches W25 F25 --output my_results.json
python find_rejected.py --output rejected_companies.json
```

## Input Format

The accepted companies file should be a JSON file with one of these formats:

**Format 1: Array of companies**
```json
[
  {
    "name": "Company Name",
    "batch": "W25",
    "description": "Optional description"
  }
]
```

**Format 2: Object with companies array**
```json
{
  "companies": [
    {
      "name": "Company Name",
      "batch": "W25"
    }
  ]
}
```

## Output Format

### YC Companies (scraper.py)
The scraper outputs a JSON file with this structure:
```json
{
  "W25": [
    {
      "name": "Company Name",
      "batch": "Winter 2025",
      "url": "https://www.ycombinator.com/companies/company-name",
      "description": "Company description",
      "website": "https://company.com"
    }
  ],
  "F25": [...]
}
```

### Rejected Companies (find_rejected.py)
```json
[
  {
    "name": "Company Name",
    "source": "TechCrunch",
    "url": "https://techcrunch.com/...",
    "title": "Article title"
  }
]
```

## Important Notes

⚠️ **This tool does not find rejected companies directly** - YC doesn't publish rejected applications. Instead:
- It scrapes companies that **were accepted** into batches
- It searches other sources (TechCrunch, Crunchbase, etc.) for companies
- It filters out any companies that ARE in YC, leaving you with companies that likely didn't get in
- This is a heuristic approach - some companies might not have applied to YC at all

⚠️ **Rate Limiting**: The scraper includes small delays between requests to be respectful to servers. Don't run aggressive scraping.

⚠️ **Website Changes**: YC's website structure may change. If the scraper stops working, you may need to update the parsing logic.

## Advanced: Using with Exa Search (Better Results)

For better results finding rejected companies, you can integrate with Exa search API:

1. Get an Exa API key from https://exa.ai
2. Add to `find_rejected.py`:
   ```python
   import exa_py as exa
   exa_client = exa.Exa(api_key="your_key")
   results = exa_client.search("AI startups 2025", num_results=100)
   ```

This will give you much better results than basic web scraping.

## Troubleshooting

- **No companies found**: 
  - YC's website structure may have changed. Check the HTML structure and update selectors
  - If the website uses JavaScript to render content, use the Playwright version:
    ```bash
    playwright install chromium
    python scraper_playwright.py --batches W25 F25
    ```
- **Connection errors**: Make sure you have internet access and websites are reachable
- **JSON errors**: Ensure your accepted companies file is valid JSON
- **JavaScript-rendered content**: If the basic scraper returns empty results, YC's website likely uses JavaScript. Use `scraper_playwright.py` instead

## Development

To extend this tool:
1. Modify `scraper.py` to handle different YC website structures
2. Add more sources to `find_rejected.py` (AngelList, LinkedIn, etc.)
3. Integrate with search APIs (Exa, Google Custom Search) for better results
4. Add machine learning to identify similar companies
