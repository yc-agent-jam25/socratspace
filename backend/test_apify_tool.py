"""
Test Apify Web Scraper Tool
Simple test to verify the tool works before implementing others

Note: Apify requires OAuth authentication. This test will:
1. Automatically create an OAuth session
2. Display a URL for you to authenticate
3. Wait for you to complete authentication
4. Then proceed with the scraping test

Usage:
    python test_apify_tool.py
"""

from tools.apify_tool import ApifyScraperTool

def test_apify_scraper():
    """Test the Apify scraper with a simple website"""

    print("=" * 60)
    print("Testing Apify Web Scraper Tool")
    print("=" * 60)
    print("\n⚠️  Note: Apify requires OAuth authentication.")
    print("   You will be prompted to authenticate when the test runs.\n")

    # Create tool instance
    tool = ApifyScraperTool()

    # Try a simple website that's easy to scrape
    # You can easily change this URL to test different sites
    test_urls = [
        "https://example.com",  # Simplest - always available, minimal content
        "https://www.wikipedia.org",  # Reliable, public content
        "https://httpbin.org/html",  # Designed specifically for testing
        "https://news.ycombinator.com",  # Simple, public site
    ]
    
    # Start with the simplest one
    test_url = test_urls[0]
    
    print(f"🌐 Test: Scraping {test_url}")
    print("-" * 60)
    print("Extract Type: all (text, links, metadata)")
    print(f"\n💡 Alternative URLs you can try (edit test_urls in this file):")
    for i, url in enumerate(test_urls[1:], 1):
        print(f"   {i}. {url}")
    print("\nNote: OAuth flow will start automatically if needed...\n")

    try:
        result = tool._run(
            url=test_url,
            extract_type="all"
        )

        # Check if result indicates an error
        if "❌" in result or "error" in result.lower() or "failed" in result.lower():
            print("\n❌ TEST FAILED - Error detected in result!")
            print("\nResult:")
            print(result)
        else:
            print("\n✅ SUCCESS!")
            print("\nResult:")
            print(result)

    except Exception as e:
        print(f"\n❌ FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_apify_scraper()
