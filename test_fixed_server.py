#!/usr/bin/env python3
"""
测试修复后的MCP服务器
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

async def test_mcp_server():
    """测试MCP服务器功能"""
    print("🧪 开始测试修复后的MCP服务器...")
    
    try:
        # 导入修复后的服务器
        from stock_advisor_server_fixed import mcp
        
        print("✅ 成功导入MCP服务器模块")
        
        # 创建模拟上下文
        class MockContext:
            async def info(self, message):
                print(f"ℹ️  {message}")
            
            async def error(self, message):
                print(f"❌ {message}")
        
        ctx = MockContext()
        
        # 测试各个工具
        print("\n📊 测试股票价格查询...")
        try:
            # 从MCP实例中获取工具
            for tool_name, tool_func in mcp._tools.items():
                if tool_name == "get_stock_price":
                    get_stock_price = tool_func
                elif tool_name == "get_stock_data":
                    get_stock_data = tool_func
                elif tool_name == "get_technical_indicators":
                    get_technical_indicators = tool_func
                elif tool_name == "search_stock_by_name":
                    search_stock_by_name = tool_func
                elif tool_name == "get_market_data":
                    get_market_data = tool_func
                elif tool_name == "get_server_status":
                    get_server_status = tool_func
            
            # 测试股票价格查询
            if get_stock_price:
                result = await get_stock_price("600136", ctx)
                print(f"✅ 股票价格查询测试通过: {result.get('name', 'N/A')} - {result.get('current_price', 0)}元")
            else:
                print("❌ 未找到get_stock_price工具")
            
            # 测试股票数据查询
            if get_stock_data:
                result = await get_stock_data("600136", ctx)
                print(f"✅ 股票数据查询测试通过: 数据质量 - {result.get('data_quality', 'N/A')}")
            else:
                print("❌ 未找到get_stock_data工具")
            
            # 测试技术指标
            if get_technical_indicators:
                result = await get_technical_indicators("600136", ctx)
                print(f"✅ 技术指标测试通过: RSI - {result.get('rsi', 0)}")
            else:
                print("❌ 未找到get_technical_indicators工具")
            
            # 测试股票搜索
            if search_stock_by_name:
                result = await search_stock_by_name("恒瑞", ctx)
                print(f"✅ 股票搜索测试通过: 找到 {len(result)} 只股票")
            else:
                print("❌ 未找到search_stock_by_name工具")
            
            # 测试市场数据
            if get_market_data:
                result = await get_market_data("600136", ctx)
                print(f"✅ 市场数据测试通过: 表现 - {result.get('performance', 'N/A')}")
            else:
                print("❌ 未找到get_market_data工具")
            
            # 测试服务器状态
            if get_server_status:
                result = await get_server_status(ctx)
                print(f"✅ 服务器状态测试通过: {result.get('status', 'N/A')}")
            else:
                print("❌ 未找到get_server_status工具")
            
            print(f"\n🎉 所有测试完成！共测试了 {len(mcp._tools)} 个工具")
            print("📋 可用工具列表:")
            for tool_name in mcp._tools.keys():
                print(f"  - {tool_name}")
            
        except Exception as e:
            print(f"❌ 工具测试失败: {e}")
            import traceback
            traceback.print_exc()
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保所有依赖都已安装: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🔧 MCP服务器测试工具")
    print("=" * 50)
    
    try:
        asyncio.run(test_mcp_server())
    except KeyboardInterrupt:
        print("\n⏹️  测试已停止")
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")

if __name__ == "__main__":
    main()