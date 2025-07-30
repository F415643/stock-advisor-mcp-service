"""
股票建议MCP服务使用示例
展示如何使用各种功能查询A股和美股信息
"""

import asyncio
from fastmcp import Client

async def demo_a_stock_analysis():
    """A股分析示例"""
    print("🇨🇳 A股分析示例")
    print("=" * 50)
    
    async with Client("stock_advisor_server.py") as client:
        
        # 1. 搜索股票
        print("\n1️⃣ 搜索股票")
        search_result = await client.call_tool("search_stock_by_name", {"name": "招商银行"})
        print(f"搜索结果: {search_result.text}")
        
        # 2. 获取股票价格
        print("\n2️⃣ 获取招商银行股价")
        price_info = await client.call_tool("get_stock_price", {"symbol": "600036"})
        print(f"价格信息: {price_info.text}")
        
        # 3. 获取股票新闻
        print("\n3️⃣ 获取相关新闻")
        news = await client.call_tool("get_stock_news", {"symbol": "600036"})
        print(f"新闻资讯: {news.text}")
        
        # 4. 综合分析
        print("\n4️⃣ 综合分析报告")
        analysis = await client.call_tool("get_comprehensive_analysis", {"symbol": "600036"})
        print(f"分析报告: {analysis.text}")

async def demo_us_stock_analysis():
    """美股分析示例"""
    print("\n🇺🇸 美股分析示例")
    print("=" * 50)
    
    async with Client("stock_advisor_server.py") as client:
        
        # 1. 获取苹果股价
        print("\n1️⃣ 获取苹果股价")
        apple_price = await client.call_tool("get_stock_price", {"symbol": "AAPL"})
        print(f"苹果股价: {apple_price.text}")
        
        # 2. 投资建议
        print("\n2️⃣ 获取投资建议")
        recommendation = await client.call_tool("get_investment_recommendation", {
            "symbol": "AAPL",
            "investment_amount": 10000,
            "risk_tolerance": "中"
        })
        print(f"投资建议: {recommendation.text}")

async def demo_market_overview():
    """市场概览示例"""
    print("\n📊 市场概览示例")
    print("=" * 50)
    
    async with Client("stock_advisor_server.py") as client:
        
        # 1. 获取热门股票
        print("\n1️⃣ 热门股票")
        hot_stocks = await client.call_tool("get_hot_stocks", {})
        print(f"热门股票: {hot_stocks.text}")
        
        # 2. 市场概况
        print("\n2️⃣ 市场概况")
        market_summary = await client.read_resource("stock://market-summary")
        print(f"市场概况: {market_summary.text}")
        
        # 3. 股票比较
        print("\n3️⃣ 股票比较")
        comparison = await client.call_tool("compare_stocks", {
            "symbols": ["000001", "600036", "000002", "600000"]
        })
        print(f"股票比较: {comparison.text}")

async def demo_interactive_query():
    """交互式查询示例"""
    print("\n🎯 交互式查询示例")
    print("=" * 50)
    
    async with Client("stock_advisor_server.py") as client:
        
        # 模拟用户查询流程
        queries = [
            ("搜索", "search_stock_by_name", {"name": "中国平安"}),
            ("价格", "get_stock_price", {"symbol": "601318"}),
            ("新闻", "get_stock_news", {"symbol": "601318"}),
            ("分析", "get_comprehensive_analysis", {"symbol": "601318"})
        ]
        
        for step, tool_name, params in queries:
            print(f"\n🔍 {step}阶段")
            try:
                result = await client.call_tool(tool_name, params)
                print(f"结果: {result.text[:200]}...")  # 只显示前200字符
            except Exception as e:
                print(f"查询失败: {e}")

async def main():
    """主函数"""
    print("🚀 股票建议MCP服务使用示例")
    print("请确保服务器正在运行...")
    
    try:
        # 运行各种示例
        await demo_a_stock_analysis()
        await demo_us_stock_analysis()
        await demo_market_overview()
        await demo_interactive_query()
        
        print("\n✅ 所有示例运行完成！")
        
    except Exception as e:
        print(f"❌ 运行示例时发生错误: {e}")
        print("请确保股票建议服务器正在运行")

if __name__ == "__main__":
    asyncio.run(main())