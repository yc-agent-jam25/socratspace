"""
Test GitHub Analyzer Tool
Test with a well-known GitHub user
"""

from tools.github_tool import GitHubAnalyzerTool

def test_github_analyzer():
    """Test GitHub analyzer with a famous developer"""

    print("=" * 60)
    print("Testing GitHub Analyzer Tool")
    print("=" * 60)

    # Create tool instance
    tool = GitHubAnalyzerTool()

    # Test with "torvalds" (Linus Torvalds - creator of Linux)
    # Guaranteed to have a great profile to analyze
    print("\n🔍 Test: Analyzing GitHub user 'torvalds'")
    print("-" * 60)

    try:
        result = tool._run(
            username="torvalds",
            include_repos=True
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
    test_github_analyzer()
