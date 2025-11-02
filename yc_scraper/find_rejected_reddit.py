"""
Find companies that did NOT get into Y Combinator using Reddit.

This is a safer heuristic because:
1. Reddit has first-hand accounts from founders
2. People often mention their company name when discussing rejections
3. r/ycombinator and related subreddits have real application stories
4. More reliable than scraping generic startup news
"""

import json
import re
import time
from pathlib import Path
from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote

import httpx
from bs4 import BeautifulSoup


class RedditRejectionFinder:
    """Finds companies that didn't get into YC by scraping Reddit."""
    
    def __init__(self, yc_companies_file: str = "yc_batch_companies.json", use_praw: bool = False):
        """Initialize with list of YC companies."""
        self.use_praw = use_praw
        self.reddit = None
        
        # Try to initialize PRAW if requested
        if use_praw:
            try:
                import praw
                import os
                
                # Get Reddit API credentials from environment
                client_id = os.getenv('REDDIT_CLIENT_ID')
                client_secret = os.getenv('REDDIT_CLIENT_SECRET')
                user_agent = os.getenv('REDDIT_USER_AGENT', 'YC Rejection Finder 1.0')
                
                if client_id and client_secret:
                    self.reddit = praw.Reddit(
                        client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent
                    )
                    print("✅ Using Reddit API (PRAW) - better rate limits and data quality")
                else:
                    print("⚠️  PRAW requested but REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET not set")
                    print("   Falling back to web scraping")
                    use_praw = False
            except ImportError:
                print("⚠️  praw not installed. Install with: pip install praw")
                print("   Falling back to web scraping")
                use_praw = False
        
        # Fallback: HTTP client for web scraping
        if not self.reddit:
            self.client = httpx.Client(timeout=30, follow_redirects=True)
            self.headers = {
                "User-Agent": "YC Rejection Finder Bot 1.0 (Educational Research)",
                "Accept": "text/html,application/json",
            }
        
        # Reddit subreddits to search
        self.subreddits = [
            "ycombinator",
            "startups",
            "entrepreneur",
            "indiebiz",
            "SaaS",
        ]
        
        # Load YC companies to filter out
        self.yc_companies = set()
        self.yc_companies_by_name = {}
        if Path(yc_companies_file).exists():
            with open(yc_companies_file, 'r') as f:
                yc_data = json.load(f)
                for batch, companies in yc_data.items():
                    for comp in companies:
                        name_lower = comp.get('name', '').lower().strip()
                        if name_lower:
                            self.yc_companies.add(name_lower)
                            self.yc_companies_by_name[name_lower] = comp
        
        print(f"📋 Loaded {len(self.yc_companies)} YC companies to filter out")
    
    def is_yc_company(self, company_name: str) -> bool:
        """Check if a company is in YC."""
        return company_name.lower().strip() in self.yc_companies
    
    def search_subreddit(self, subreddit: str, query: str = "", limit: int = 100) -> List[Dict]:
        """
        Search a subreddit for posts about YC applications/rejections.
        
        Uses PRAW if available, otherwise falls back to web scraping.
        """
        print(f"\n🔍 Searching r/{subreddit}...")
        posts = []
        
        try:
            # Use PRAW if available
            if self.reddit:
                try:
                    sub = self.reddit.subreddit(subreddit)
                    
                    if query:
                        # Search with query
                        for submission in sub.search(query, limit=limit, sort='relevance'):
                            posts.append({
                                'title': submission.title,
                                'selftext': submission.selftext,
                                'url': submission.url,
                                'permalink': f"https://reddit.com{submission.permalink}",
                                'created_utc': submission.created_utc,
                                'score': submission.score,
                                'num_comments': submission.num_comments,
                                'subreddit': subreddit,
                                'comments': self._get_top_comments(submission, limit=10),  # Get comments too
                            })
                    else:
                        # Get top posts
                        for submission in sub.hot(limit=limit):
                            posts.append({
                                'title': submission.title,
                                'selftext': submission.selftext,
                                'url': submission.url,
                                'permalink': f"https://reddit.com{submission.permalink}",
                                'created_utc': submission.created_utc,
                                'score': submission.score,
                                'num_comments': submission.num_comments,
                                'subreddit': subreddit,
                                'comments': self._get_top_comments(submission, limit=10),
                            })
                except Exception as e:
                    print(f"  ⚠️  PRAW error: {e}")
                    return []
            
            # Fallback: Web scraping
            else:
                # Reddit search URL
                if query:
                    search_url = f"https://old.reddit.com/r/{subreddit}/search.json"
                    params = {
                        "q": query,
                        "restrict_sr": "1",
                        "limit": limit,
                        "sort": "relevance"
                    }
                else:
                    # Get top posts from subreddit
                    search_url = f"https://old.reddit.com/r/{subreddit}/.json"
                    params = {"limit": limit}
                
                # Try JSON API first (better structured)
                try:
                    response = self.client.get(search_url, headers=self.headers, params=params)
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'data' in data and 'children' in data['data']:
                                for child in data['data']['children']:
                                    post_data = child.get('data', {})
                                    posts.append({
                                        'title': post_data.get('title', ''),
                                        'selftext': post_data.get('selftext', ''),
                                        'url': post_data.get('url', ''),
                                        'permalink': f"https://reddit.com{post_data.get('permalink', '')}",
                                        'created_utc': post_data.get('created_utc', 0),
                                        'score': post_data.get('score', 0),
                                        'num_comments': post_data.get('num_comments', 0),
                                        'subreddit': subreddit,
                                    })
                        except json.JSONDecodeError:
                            # Fall back to HTML scraping
                            pass
                except:
                    pass
                
                # Fallback: HTML scraping
                if not posts:
                    html_url = f"https://old.reddit.com/r/{subreddit}/"
                    if query:
                        html_url = f"https://old.reddit.com/r/{subreddit}/search?q={quote(query)}&restrict_sr=on"
                    
                    response = self.client.get(html_url, headers=self.headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Find post links
                        post_links = soup.find_all('a', class_='title', href=re.compile(r'/r/'))
                        
                        for link in post_links[:limit]:
                            title = link.get_text(strip=True)
                            href = link.get('href', '')
                            if href.startswith('/'):
                                href = f"https://old.reddit.com{href}"
                            
                            posts.append({
                                'title': title,
                                'url': href,
                                'subreddit': subreddit,
                            })
            
            print(f"  Found {len(posts)} posts in r/{subreddit}")
            return posts
            
        except Exception as e:
            print(f"  ⚠️  Error searching r/{subreddit}: {e}")
            return []
    
    def _get_top_comments(self, submission, limit: int = 10) -> List[str]:
        """Get top comments from a submission (for PRAW)."""
        comments = []
        try:
            submission.comments.replace_more(limit=0)  # Remove "more comments" links
            for comment in submission.comments.list()[:limit]:
                if hasattr(comment, 'body') and comment.body:
                    comments.append(comment.body)
        except:
            pass
        return comments
    
    def extract_companies_from_text(self, text: str, title: str = "", comments: List[str] = None) -> List[str]:
        """
        Extract company names from Reddit posts/comments.
        
        Looks for patterns like:
        - "My company [Name] got rejected"
        - "We applied as [Company]"
        - "[Company] didn't get in"
        - "I know [Company] that got rejected"
        - Comments mentioning companies
        """
        companies = []
        
        # Combine all text sources
        all_text_parts = [title, text]
        if comments:
            all_text_parts.extend(comments)
        full_text = " ".join(all_text_parts)
        full_text_lower = full_text.lower()
        
        # Patterns that indicate company names (including third-person mentions)
        patterns = [
            # First person: "My company X"
            r'(?:my|our|the) (?:company|startup|product|app|service) (?:is|was|called|named)\s+([A-Z][a-zA-Z0-9\s&]{2,30})',
            r'(?:company|startup|app|product|service) (?:named|called|is|was)\s+([A-Z][a-zA-Z0-9\s&]{2,30})',
            
            # Direct rejection mentions
            r'([A-Z][a-zA-Z0-9\s&]{2,30}) (?:didn\'t|did not|wasn\'t|was not) (?:get|make|accept) (?:in|into|through)',
            r'([A-Z][a-zA-Z0-9\s&]{2,30}) (?:got|was) (?:rejected|denied|turned down)',
            r'([A-Z][a-zA-Z0-9\s&]{2,30}) (?:wasn\'t|was not) (?:accepted|selected)',
            
            # Third person: "Company X got rejected" or "I know X that..."
            r'(?:i|we|they) (?:know|saw|heard|met|know of) (?:a company|startup|someone) (?:named|called)?\s+([A-Z][a-zA-Z0-9\s&]{2,30})',
            r'(?:i|we) (?:know|saw|heard) ([A-Z][a-zA-Z0-9\s&]{2,30}) (?:got|was) (?:rejected|didn\'t get)',
            
            # Rejection context
            r'rejected (?:from|by|at) (?:yc|ycombinator).*?([A-Z][a-zA-Z0-9\s&]{2,30})',
            r'([A-Z][a-zA-Z0-9\s&]{2,30}) (?:applied|tried) (?:to|for) (?:yc|ycombinator)',
            r'applied (?:as|with)\s+([A-Z][a-zA-Z0-9\s&]{2,30})',
            r'YC (?:rejected|denied|didn\'t accept|did not accept) (?:us|our company|them|their company)?\s*([A-Z][a-zA-Z0-9\s&]{2,30})?',
            
            # Mentioning companies in comments/discussions
            r'([A-Z][a-zA-Z0-9\s&]{2,30}) (?:also|didn\'t|wasn\'t) (?:applied|get|make it)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, full_text, re.IGNORECASE)
            for match in matches:
                company = match.group(1) if match.lastindex >= 1 and match.group(1) else None
                if not company and match.group(0):
                    # Fallback: extract from full match
                    company = match.group(0)
                
                if company:
                    # Clean up company name
                    company = company.strip()
                    
                    # Remove trailing punctuation and common stop words
                    company = re.sub(r'[,;:!?.]+$', '', company)  # Remove trailing punctuation
                    company = re.sub(r'\s+(got|was|is|are|the|a|an|our|my|also|didn\'t|did not|wasn\'t|was not|applied|got|was|that|which|they|them|their)\s+', ' ', company, flags=re.I)
                    company = company.strip()
                    
                    # Remove common prefixes/suffixes
                    company = re.sub(r'^(my|our|the|a|an|i|we|they)\s+', '', company, flags=re.I)
                    company = re.sub(r'\s+(got|was|is|are|got|rejected|denied|didn\'t|applied|company|startup)$', '', company, flags=re.I)
                    company = company.strip()
                    
                    # Basic validation
                    if (len(company) >= 2 and len(company) <= 50 and 
                        not company.lower() in ['yc', 'ycombinator', 'company', 'startup', 'app', 'product', 'service', 'the', 'a', 'an'] and
                        not re.match(r'^(my|our|the|a|an|i|we|they)\s+', company, re.I) and
                        # Must have at least one letter
                        re.search(r'[a-zA-Z]', company)):
                        companies.append(company)
        
        # Also look for capitalized phrases that might be company names
        # After keywords like "rejected", "didn't get in", etc.
        rejection_keywords = ['rejected', "didn't get", "didn't make", 'denied', 'not accepted']
        for keyword in rejection_keywords:
            idx = full_text.find(keyword)
            if idx != -1:
                # Extract text after keyword
                after_text = full_text[idx + len(keyword):idx + len(keyword) + 100]
                # Look for capitalized words (potential company names)
                capitalized_matches = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', after_text)
                for match in capitalized_matches:
                    if len(match) >= 3 and len(match) <= 30:
                        companies.append(match)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_companies = []
        for comp in companies:
            comp_lower = comp.lower()
            if comp_lower not in seen and comp_lower:
                seen.add(comp_lower)
                unique_companies.append(comp)
        
        return unique_companies
    
    def search_rejections(self, batch_year: int = 2025, limit_per_sub: int = 50) -> List[Dict]:
        """
        Search Reddit for posts about YC rejections.
        
        Args:
            batch_year: Year of the batch (to filter by time)
            limit_per_sub: Max posts per subreddit
        """
        print(f"\n🔍 Searching Reddit for YC rejection stories (batch {batch_year})...")
        
        # Search queries
        queries = [
            f"YC rejected {batch_year}",
            f"Y Combinator rejected {batch_year}",
            f"didn't get into YC {batch_year}",
            f"YC application rejected",
            f"Y Combinator rejection",
            "YC didn't accept",
            "YC rejection story",
        ]
        
        all_posts = []
        
        # Search each subreddit with different queries
        for subreddit in self.subreddits:
            for query in queries:
                posts = self.search_subreddit(subreddit, query, limit_per_sub)
                all_posts.extend(posts)
                time.sleep(1)  # Be respectful to Reddit
        
        # Remove duplicates
        seen_urls = set()
        unique_posts = []
        for post in all_posts:
            url = post.get('permalink') or post.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_posts.append(post)
        
        print(f"\n📦 Found {len(unique_posts)} unique Reddit posts about YC")
        
        # Extract companies from posts AND comments
        companies_found = []
        for post in unique_posts:
            title = post.get('title', '')
            text = post.get('selftext', '')
            comments = post.get('comments', [])  # From PRAW
            
            companies = self.extract_companies_from_text(text, title, comments)
            
            for company in companies:
                if not self.is_yc_company(company):
                    companies_found.append({
                        'name': company,
                        'source': 'Reddit',
                        'subreddit': post.get('subreddit', ''),
                        'post_title': title[:200],
                        'post_url': post.get('permalink') or post.get('url', ''),
                        'post_score': post.get('score', 0),
                        'post_comments': post.get('num_comments', 0),
                        'extracted_from': 'title' if company.lower() in title.lower() else 'body',
                    })
        
        # Remove duplicates
        seen = set()
        unique_companies = []
        for comp in companies_found:
            name_lower = comp['name'].lower()
            if name_lower not in seen:
                seen.add(name_lower)
                unique_companies.append(comp)
        
        print(f"✅ Extracted {len(unique_companies)} unique companies from Reddit posts")
        
        return unique_companies
    
    def save_results(self, companies: List[Dict], output_file: str = "rejected_companies_reddit.json"):
        """Save results to JSON file."""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(companies, f, indent=2)
        print(f"\n💾 Results saved to {output_path}")
    
    def close(self):
        """Close HTTP client."""
        self.client.close()


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find companies that didn't get into YC using Reddit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python find_rejected_reddit.py
  
  # Specify batch year
  python find_rejected_reddit.py --year 2025
  
  # Custom subreddits
  python find_rejected_reddit.py --subreddits ycombinator startups
        """
    )
    
    parser.add_argument('--yc-file', type=str, default='yc_batch_companies.json',
                       help='File with YC companies (to filter out)')
    parser.add_argument('--year', type=int, default=2025,
                       help='Batch year to search around')
    parser.add_argument('--subreddits', nargs='+',
                       default=None,
                       help='Subreddits to search (default: ycombinator, startups, entrepreneur, etc.)')
    parser.add_argument('--limit', type=int, default=50,
                       help='Max posts per subreddit')
    parser.add_argument('--output', type=str, default='rejected_companies_reddit.json',
                       help='Output file')
    parser.add_argument('--use-praw', action='store_true',
                       help='Use PRAW (Reddit API) instead of web scraping (requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET env vars)')
    
    args = parser.parse_args()
    
    # Check if PRAW should be used
    use_praw = args.use_praw
    if use_praw:
        import os
        if not (os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET')):
            print("⚠️  --use-praw specified but REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET not set")
            print("   Falling back to web scraping")
            use_praw = False
    
    finder = RedditRejectionFinder(yc_companies_file=args.yc_file, use_praw=use_praw)
    
    if args.subreddits:
        finder.subreddits = args.subreddits
    
    try:
        companies = finder.search_rejections(
            batch_year=args.year,
            limit_per_sub=args.limit
        )
        
        finder.save_results(companies, args.output)
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"\nFound {len(companies)} companies that are NOT in YC batches")
        
        if companies:
            print(f"\nSample companies found on Reddit:")
            for comp in companies[:10]:
                print(f"\n  🏢 {comp['name']}")
                print(f"     📍 r/{comp['subreddit']}")
                print(f"     📝 {comp['post_title'][:60]}...")
                print(f"     🔗 {comp['post_url']}")
        else:
            print("\n⚠️  No companies found. This could mean:")
            print("   - Reddit API rate limiting")
            print("   - No recent rejection posts")
            print("   - Company name extraction needs tuning")
            print("\n💡 Try:")
            print("   - Increasing --limit")
            print("   - Adding more subreddits")
            print("   - Checking Reddit accessibility")
        
    finally:
        finder.close()


if __name__ == "__main__":
    main()

