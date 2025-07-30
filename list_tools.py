import asyncio
from stock_advisor_server import mcp

async def list_tools():
    tools = await mcp.get_tools()
    print("Available tools:")
    for tool in tools:
        print(tool)

if __name__ == "__main__":
    asyncio.run(list_tools())