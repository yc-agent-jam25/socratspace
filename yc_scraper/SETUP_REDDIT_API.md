# Setting Up Reddit API (PRAW) for Better Results

Using Reddit's official API (via PRAW) gives you:
- ✅ Better rate limits (60 requests/minute vs scraping limits)
- ✅ Access to comments (where company names are often mentioned)
- ✅ More reliable data structure
- ✅ No need to parse HTML

## Quick Setup

### 1. Create Reddit App

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..." at the bottom
3. Fill in:
   - **Name**: YC Rejection Finder (or any name)
   - **Type**: script
   - **Description**: Educational research tool
   - **Redirect URI**: http://localhost:8080 (or any valid URL)
4. Click "create app"
5. Note your **client ID** (under the app name, looks like random chars)
6. Note your **secret** (the "secret" field)

### 2. Set Environment Variables

```bash
export REDDIT_CLIENT_ID="your_client_id_here"
export REDDIT_CLIENT_SECRET="your_secret_here"
export REDDIT_USER_AGENT="YC Rejection Finder 1.0 by /u/yourusername"
```

Or add to your `.env` file:
```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT="YC Rejection Finder 1.0 by /u/yourusername"
```

### 3. Use PRAW

```bash
python find_rejected_reddit.py --use-praw --yc-file yc_batch_companies.json
```

## Why This Helps with Edge Cases

### 1. **Comments Are Gold**
Many company mentions are in comments, not posts:
- "I know [Company X] that got rejected"
- "Yeah, [Company Y] didn't make it either"
- Comments on rejection posts often mention other companies

PRAW gives you easy access to comments, web scraping doesn't.

### 2. **Better Pattern Matching**
With structured data, you can:
- Search across post titles, bodies, AND comments
- Extract company names from nested comment threads
- Access metadata (score, engagement) to filter quality

### 3. **Rate Limits**
Reddit API: 60 requests/minute
Web scraping: Often blocked after a few requests

## Example: Finding Companies in Comments

With PRAW enabled, the scraper automatically:
1. Gets top posts about YC rejections
2. Downloads top comments from each post
3. Extracts company names from comments too

**Example comment:**
> "I know a company called DataFlow that applied for W25 but didn't get in. They're doing AI for logistics."

The scraper will extract "DataFlow" from this comment.

## Troubleshooting

### "PRAW error: 401 Unauthorized"
- Check that `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` are set correctly
- Make sure you're using the client ID (not the name) and secret

### "PRAW error: 403 Forbidden"
- Check that your `REDDIT_USER_AGENT` includes your Reddit username
- Format: `"YC Rejection Finder 1.0 by /u/yourusername"`

### "praw not installed"
```bash
pip install praw
```

## Without PRAW (Web Scraping Fallback)

If you don't set up PRAW, the scraper will still work using web scraping:
- Uses `old.reddit.com` (more scraping-friendly)
- Gets posts but NOT comments
- May hit rate limits faster
- Still functional, just less comprehensive

The scraper automatically falls back to web scraping if PRAW isn't configured.

