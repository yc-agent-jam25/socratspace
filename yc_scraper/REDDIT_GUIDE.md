# Finding Rejected YC Companies via Reddit

This is a **safer and more reliable heuristic** for finding companies that didn't get into Y Combinator.

## Why Reddit is Better

### 1. First-Hand Accounts
Reddit has real founders posting about their YC application experience:
- People share rejection stories
- They mention their company name
- Often include context about why they think they were rejected

### 2. Targeted Communities
Subreddits like r/ycombinator, r/startups have:
- Application threads
- Rejection discussion posts
- "Didn't get in" stories

### 3. Better Signal-to-Noise
Unlike generic startup news, Reddit posts are:
- Directly about YC applications
- Written by actual applicants
- Often include company details

## How It Works

The Reddit scraper:
1. Searches relevant subreddits for posts about YC rejections
2. Extracts company names from posts using pattern matching
3. Filters out companies that ARE in YC batches
4. Returns companies mentioned in rejection stories

## Usage

### Basic Usage

```bash
python find_rejected_reddit.py --yc-file yc_batch_companies.json --year 2025
```

### Custom Subreddits

Search specific subreddits:

```bash
python find_rejected_reddit.py \
    --yc-file yc_batch_companies.json \
    --year 2025 \
    --subreddits ycombinator startups entrepreneur
```

### Increase Search Depth

Get more posts:

```bash
python find_rejected_reddit.py \
    --yc-file yc_batch_companies.json \
    --year 2025 \
    --limit 100
```

## Example Results

```json
[
  {
    "name": "AcmeAI",
    "source": "Reddit",
    "subreddit": "ycombinator",
    "post_title": "Didn't get into YC W25 - here's what happened",
    "post_url": "https://reddit.com/r/ycombinator/...",
    "post_score": 45,
    "post_comments": 12,
    "extracted_from": "body"
  }
]
```

## What to Look For

The scraper extracts company names from patterns like:
- "My company [Name] got rejected"
- "We applied as [Company]"
- "[Company] didn't get in"
- "YC rejected [Company]"

## Limitations

1. **Not everyone posts on Reddit**: Some founders don't discuss rejections publicly
2. **Name extraction isn't perfect**: May miss some or extract false positives
3. **Reddit rate limiting**: May need to slow down requests
4. **Privacy**: Some posts don't mention company names

## Tips for Better Results

### 1. Check Multiple Subreddits
```bash
python find_rejected_reddit.py \
    --subreddits ycombinator startups entrepreneur SaaS indiebiz
```

### 2. Focus on Recent Batches
Search for specific batches:
- W25 posts are most likely to mention W25 applications
- F25 posts are most likely to mention F25 applications

### 3. Manual Verification
Review the posts yourself:
```bash
# Open the output file
cat rejected_companies_reddit.json

# Visit the Reddit posts to verify
# Check if companies actually applied and got rejected
```

### 4. Combine with Other Methods
Use Reddit as primary source, supplement with:
- Exa search for news articles
- Twitter/X mentions
- LinkedIn posts

## Rate Limiting

Reddit has rate limits. If you get blocked:
- Slow down requests (already built in with `time.sleep`)
- Use Reddit API with authentication (better approach)
- Consider using PRAW (Python Reddit API Wrapper)

## Advanced: Using PRAW

For better results, use Reddit's official API:

```python
import praw

reddit = praw.Reddit(
    client_id="your_id",
    client_secret="your_secret",
    user_agent="YC Rejection Finder 1.0"
)

# Search r/ycombinator
for submission in reddit.subreddit("ycombinator").search("YC rejected 2025"):
    # Process submission
    pass
```

## Verification Workflow

1. **Run scraper**: Get initial list
2. **Manual review**: Check Reddit posts for context
3. **Verify company**: Confirm company exists and matches description
4. **Filter false positives**: Remove companies that:
   - Didn't actually apply to YC
   - Are mentioned in unrelated contexts
   - Are ambiguous or unclear

## Comparison to Other Methods

| Method | Reliability | Completeness | Effort |
|--------|------------|--------------|--------|
| **Reddit** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Low |
| Generic News | ⭐⭐ | ⭐⭐⭐⭐ | Low |
| Exa Search | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium |
| Manual Research | ⭐⭐⭐⭐⭐ | ⭐⭐ | High |

**Reddit is best balance** of reliability and completeness for finding rejected companies.

