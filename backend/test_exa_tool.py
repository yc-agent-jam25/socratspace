"""
Test Exa AI Search Tool
Test with a relevant investment research query
"""

from tools.exa_tool import ExaSearchTool

def test_exa_search():
    """Test Exa AI search with an investment-related query"""

    print("=" * 60)
    print("Testing Exa AI Search Tool")
    print("=" * 60)

    # Create tool instance
    tool = ExaSearchTool()

    # Test with AI/ML infrastructure query
    print("\n🔍 Test: Searching for 'AI infrastructure startups'")
    print("-" * 60)

    try:
        result = tool._run(
            query="AI infrastructure startups funding trends 2024",
            num_results=5
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
    test_exa_search()
