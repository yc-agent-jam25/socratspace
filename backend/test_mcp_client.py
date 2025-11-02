"""
Test MCP client connectivity
"""
import asyncio
from tools.mcp_client import mcp_client

async def test_connection():
    """Test basic MCP connectivity with HackerNews (simplest)"""
    try:
        print("Testing MCP connection...")
        print("Calling HackerNews get_best_stories tool...")

        # Test HackerNews get_best_stories (from your dashboard screenshot)
        result = await mcp_client.call_mcp(
            mcp_name="hackernews",
            tool_name="get_best_stories",
            parameters={"limit": 5}
        )

        print("✅ MCP Connection Successful!")
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        return True

    except Exception as e:
        print(f"❌ MCP Connection Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
