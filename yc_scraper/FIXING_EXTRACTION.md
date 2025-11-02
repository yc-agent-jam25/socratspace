# The Problem with Company Name Extraction

You're absolutely right - **almost none of the extracted "names" are actual company names**. The extraction patterns in the Reddit scraper are way too loose and picking up random words/phrases.

## What Went Wrong

The regex patterns in `find_rejected_reddit.py` are matching:
- Random capitalized words in sentences ("And", "But", "The")
- Partial phrases ("all about", "just made")
- Common words that happen to be capitalized
- Fragments of sentences

## Why This Happens

1. **People don't always mention company names**: When discussing YC rejections, founders often say "we got rejected" without naming their company
2. **Natural language is messy**: Regex can't reliably distinguish company names from regular capitalized words
3. **Patterns are too greedy**: The regex matches anything capitalized, not just proper nouns

## Potential Real Companies Found

From scanning the actual posts, only a few look potentially real:
- **Veed** - Actually mentioned in a post ("we bootstrapped Veed")
- **RapidAPI** - Appears to be a real company name
- **Rappi** - Mentioned in posts (Rappi is a real Latin American delivery company)
- **Konsus** - Might be real (Konsus was a YC company, but this might be a false match)

## Better Approaches

### Option 1: Manual Review of Reddit Posts
The JSON has the actual Reddit URLs. You could:
1. Review posts manually
2. Look for real company names in the post titles/bodies
3. Extract only the ones that are clearly company names

### Option 2: Use NLP/ML
- Use a named entity recognition (NER) model
- Train/fine-tune on startup company names
- More accurate than regex

### Option 3: Different Data Source
- **Twitter/X**: Founders sometimes tweet about rejections with company name
- **LinkedIn**: Posts about YC applications often include company name
- **YC Application Forums**: Public discussions might mention companies
- **AngelList/Product Hunt**: Companies that list but aren't YC-backed

### Option 4: Look for Links/URLs
Many posts mention company websites. Extract domains:
- "Check out our product at companyname.com"
- Links in Reddit posts
- Domain names are more reliable than company name extraction

## Quick Fix: Extract Domains Instead

Instead of extracting company names, extract domains/websites mentioned in posts:

```python
# Look for URLs in posts
url_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\.(?:com|io|ai|co|net)'
# This would find domains like "companyname.com"
```

## Recommendation

**The current extraction is too unreliable.** I'd recommend:

1. **Scraping actual Reddit posts** to get full text
2. **Looking for URLs/domains** mentioned (more reliable)
3. **Using NLP** to identify proper nouns that might be company names
4. **Manual verification** for accuracy

Or use a completely different approach - don't rely on Reddit extraction for company names. Instead, use it to find posts, then manually review or use a different method to extract the names.

Would you like me to:
1. Create a domain/URL extractor instead?
2. Set up NLP-based extraction?
3. Create a tool to help manually review the Reddit posts?

