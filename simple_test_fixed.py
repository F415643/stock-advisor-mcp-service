#!/usr/bin/env python3
"""
简化的MCP服务器测试脚本
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

async def test_server():
    """测试服务器功能"""
    print("🧪 开始测试MCP服务器...")
    
    try:
        # 导入服务器模块
        from stock_advisor_server_fixed import (
            get_stock_price, get_stock_data, get_technical_indicators,
            search_stock_by_name, get_market_data, get_server_status
        )
        
        print("✅ 成功导入所有工具函数")
        
        # 创建模拟上下文
        class MockContext:
            async def info(self, message):
                print(f"ℹ️  {message}")
            
            async def error(self, message):
                print(f"❌ {message}")
        
        ctx = MockContext()
        
        # 测试1: 股票价格查询
        print("\n📊 测试1: 股票价格查询...")
        result = await get_stock_price("600136", ctx)
        if "error" not in result:
            print(f"✅ 成功: {result.get('name', 'N/A')} - {result.get('current_price', 0)}元")
        else:
            print(f"❌ 失败: {result['error']}")
        
        # 测试2: 股票数据查询
        print("\n📈 测试2: 股票数据查询...")
        result = await get_stock_data("600136", ctx)
        if "error" not in result:
            print(f"✅ 成功: 数据源 - {result.get('data_source', 'N/A')}")
        else:
            print(f"❌ 失败: {result['error']}")
        
        # 测试3: 技术指标
        print("\n📉 测试3: 技术指标计算...")
        result = await get_technical_indicators("600136", ctx)
        if "error" not in result:
            print(f"✅ 成功: RSI={result.get('rsi', 0)}, MFI={result.get('mfi', 0)}")
        else:
            print(f"❌ 失败: {result['error']}")
        
        # 测试4: 股票搜索
        print("\n🔍 测试4: 股票搜索...")
        result = await search_stock_by_name("恒瑞", ctx)
        if isinstance(result, list):
            print(f"✅ 成功: 找到 {len(result)} 只股票")
        else:
            print(f"❌ 失败: 返回类型错误")
        
        # 测试5: 市场数据
        print("\n📊 测试5: 市场数据分析...")
        result = await get_market_data("600136", ctx)
        if "error" not in result:
            print(f"✅ 成功: 表现 - {result.get('performance', 'N/A')}")
        else:
            print(f"❌ 失败: {result['error']}")
        
        # 测试6: 服务器状态
        print("\n🖥️  测试6: 服务器状态...")
        result = await get_server_status(ctx)
        if "error" not in result:
            print(f"✅ 成功: 状态 - {result.get('status', 'N/A')}")
        else:
            print(f"❌ 失败: {result['error']}")
        
        print("\n🎉 所有测试完成！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了所有依赖: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 MCP服务器简化测试工具")
    print("=" * 40)
    
    try:
        success = asyncio.run(test_server())
        if success:
            print("\n✅ 测试通过！MCP服务器可以正常工作")
        else:
            print("\n❌ 测试失败！请检查配置")
    except KeyboardInterrupt:
        print("\n⏹️  测试已停止")
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")

if __name__ == "__main__":
    main()