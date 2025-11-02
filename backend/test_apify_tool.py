"""
Test Apify Web Scraper Tool
Simple test to verify the tool works before implementing others
"""

from tools.apify_tool import ApifyScraperTool

def test_apify_scraper():
    """Test the Apify scraper with a simple website"""

    print("=" * 60)
    print("Testing Apify Web Scraper Tool")
    print("=" * 60)

    # Create tool instance
    tool = ApifyScraperTool()

    # Test with example.com (simple, always available)
    print("\n🌐 Test 1: Scraping example.com")
    print("-" * 60)

    try:
        result = tool._run(
            url="https://meta.com",
            extract_type="all"
        )

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
