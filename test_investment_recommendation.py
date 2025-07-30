"""
测试投资建议工具的简单脚本
"""

import asyncio
from fastmcp import Client

async def test_investment_recommendation():
    """测试投资建议工具"""
    print("🔍 测试投资建议工具...")
    
    try:
        # 连接到股票建议服务
        async with Client("stock_advisor_server.py") as client:
            # 获取投资建议
            print("\n💡 获取投资建议")
            result = await client.call_tool("get_investment_recommendation", {
                "symbol": "600975",
                "investment_amount": 10000,
                "risk_tolerance": "中"
            })
            
            print(f"结果: {result}")
            
            # 检查结果内容
            if hasattr(result, 'content'):
                print(f"内容: {result.content}")
            if hasattr(result, 'text'):
                print(f"文本: {result.text}")
                
    except Exception as e:
        print(f"❌ 测试投资建议工具时出错: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    await test_investment_recommendation()

if __name__ == "__main__":
    asyncio.run(main())