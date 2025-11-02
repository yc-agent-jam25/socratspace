"""
Test LinkedIn Profile Analyzer Tool
Test with a LinkedIn username
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.tools.linkedin_tool import LinkedInAnalyzerTool
except ImportError:
    from tools.linkedin_tool import LinkedInAnalyzerTool

from dotenv import load_dotenv

load_dotenv()

def test_linkedin_analyzer():
    """Test LinkedIn analyzer with a LinkedIn username"""

    print("=" * 60)
    print("Testing LinkedIn Profile Analyzer Tool")
    print("=" * 60)

    # Check configuration
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    mcp_linkedin_id = os.getenv("MCP_LINKEDIN_ID")
    
    print("\n📋 Configuration Check:")
    print(f"  RAPIDAPI_KEY: {'✅ Set' if rapidapi_key else '❌ Not set'}")
    print(f"  MCP_LINKEDIN_ID: {'✅ Set' if mcp_linkedin_id else '❌ Not set'}")
    
    if not rapidapi_key and not mcp_linkedin_id:
        print("\n⚠️  WARNING: Neither RAPIDAPI_KEY nor MCP_LINKEDIN_ID is set.")
        print("   The tool will show a configuration message instead of analyzing profiles.")
        print("\n   To get started:")
        print("   1. Get RapidAPI key from: https://rapidapi.com/")
        print("   2. Subscribe to LinkedIn Data API")
        print("   3. Add RAPIDAPI_KEY=your_key to .env file")
        print()

    # Create tool instance
    tool = LinkedInAnalyzerTool()

    # Test with a LinkedIn username (you can change this)
    # Format: just the username part, e.g., "john-doe" or "in/john-doe"
    test_username = "billgates"  # Bill Gates - likely to have posts
    
    print(f"\n🔍 Test: Analyzing LinkedIn user '{test_username}'")
    print("-" * 60)

    try:
        result = tool._run(
            username=test_username,
            analyze_posts=True,
            top_n=5
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
    print("\n💡 Tips:")
    print("  - LinkedIn usernames can be:")
    print("    • Just the username: 'billgates'")
    print("    • Full URL format: 'in/billgates'")
    print("  - Some profiles may be private or have no posts")
    print("  - Check your RapidAPI subscription limits if you get rate limit errors")

if __name__ == "__main__":
    test_linkedin_analyzer()

