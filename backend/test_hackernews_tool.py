"""
Test HackerNews Search Tool
Test with a real topic that should have discussions
"""

from tools.hackernews_tool import HackerNewsSearchTool

def test_hackernews_search():
    """Test HackerNews search with a popular tech topic"""

    print("=" * 60)
    print("Testing HackerNews Search Tool")
    print("=" * 60)

    # Create tool instance
    tool = HackerNewsSearchTool()

    # Test with "AI" - guaranteed to have discussions
    print("\n🔍 Test: Searching HackerNews for 'OpenAI'")
    print("-" * 60)

    try:
        result = tool._run(
            query="OpenAI",
            limit=5
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
    test_hackernews_search()
