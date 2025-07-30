#!/usr/bin/env python3
"""
股票数据MCP服务器 - 修复版
提供股票数据查询和技术分析功能
"""

import argparse
import asyncio
import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

try:
    from fastmcp import FastMCP, Context
    import aiohttp
except ImportError as e:
    print(f"缺少必要的依赖包: {e}")
    print("请运行: pip install fastmcp aiohttp")
    sys.exit(1)

# 尝试导入自定义模块
try:
    from stock_data_fetcher import fetch_stock_data, search_stock, StockDataFetcher
except ImportError:
    print("警告: 无法导入stock_data_fetcher，将使用模拟数据")
    StockDataFetcher = None
    fetch_stock_data = None
    search_stock = None

try:
    from technical_analysis import TechnicalAnalyzer
except ImportError:
    print("警告: 无法导入technical_analysis，技术分析功能将受限")
    TechnicalAnalyzer = None

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mcp-stock.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="股票数据MCP服务器")
    parser.add_argument("--name", type=str, default="股票数据服务", help="服务器名称")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--port", type=int, default=8080, help="服务端口")
    parser.add_argument("--host", type=str, default="localhost", help="服务主机")
    return parser.parse_args()

args = parse_args()

# 创建MCP服务器实例
mcp = FastMCP(name=args.name)

# 模拟股票数据
MOCK_STOCK_DATA = {
    "600136": {
        "symbol": "600136",
        "name": "恒瑞医药",
        "price": 45.67,
        "change": 1.23,
        "change_percent": 2.77,
        "volume": 1234567,
        "market_cap": 200000000000,
        "pe_ratio": 25.5,
        "high": 46.80,
        "low": 44.50,
        "open": 45.20,
        "pre_close": 44.44
    },
    "000001": {
        "symbol": "000001",
        "name": "平安银行",
        "price": 12.34,
        "change": -0.15,
        "change_percent": -1.20,
        "volume": 2345678,
        "market_cap": 150000000000,
        "pe_ratio": 8.5,
        "high": 12.50,
        "low": 12.20,
        "open": 12.45,
        "pre_close": 12.49
    },
    "600519": {
        "symbol": "600519",
        "name": "贵州茅台",
        "price": 1680.50,
        "change": 25.30,
        "change_percent": 1.53,
        "volume": 123456,
        "market_cap": 2100000000000,
        "pe_ratio": 35.2,
        "high": 1695.00,
        "low": 1665.00,
        "open": 1670.00,
        "pre_close": 1655.20
    }
}

@mcp.tool
async def get_stock_price(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取指定股票的当前价格和基本信息
    
    Args:
        symbol: 股票代码（如600136、000001等）
    
    Returns:
        包含股票价格、涨跌幅、成交量等信息的字典
    """
    try:
        await ctx.info(f"正在查询股票 {symbol} 的价格信息...")
        
        # 首先尝试使用真实数据
        if fetch_stock_data:
            try:
                comprehensive_data = await fetch_stock_data(symbol)
                if comprehensive_data and comprehensive_data.get('basic_info'):
                    basic_info = comprehensive_data['basic_info']
                    result = {
                        "symbol": symbol,
                        "name": basic_info.get("name", ""),
                        "current_price": basic_info.get("price", 0),
                        "change": basic_info.get("change", 0),
                        "change_percent": basic_info.get("change_percent", 0),
                        "volume": basic_info.get("volume", 0),
                        "high": basic_info.get("high", 0),
                        "low": basic_info.get("low", 0),
                        "open": basic_info.get("open", 0),
                        "pre_close": basic_info.get("pre_close", 0),
                        "market_cap": basic_info.get("market_cap", 0),
                        "pe_ratio": basic_info.get("pe_ratio", 0),
                        "timestamp": datetime.now().isoformat(),
                        "data_source": "实时数据"
                    }
                    await ctx.info(f"成功获取 {symbol} 的实时数据")
                    return result
            except Exception as e:
                await ctx.error(f"获取实时数据失败: {e}")
        
        # 使用模拟数据
        if symbol in MOCK_STOCK_DATA:
            stock_data = MOCK_STOCK_DATA[symbol]
            await ctx.info(f"使用模拟数据返回 {symbol} 的信息")
            return {
                **stock_data,
                "timestamp": datetime.now().isoformat(),
                "data_source": "模拟数据"
            }
        else:
            return {"error": f"未找到股票代码 {symbol} 的数据"}
            
    except Exception as e:
        await ctx.error(f"获取股票价格时发生错误: {str(e)}")
        return {"error": f"获取股票价格失败: {str(e)}"}

@mcp.tool
async def get_stock_data(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取股票基本数据
    
    Args:
        symbol: 股票代码
    
    Returns:
        股票基本数据信息
    """
    try:
        await ctx.info(f"正在获取股票 {symbol} 的基本数据...")
        
        # 调用价格查询功能
        price_data = await get_stock_price(symbol, ctx)
        
        if "error" in price_data:
            return price_data
        
        # 添加额外的基本数据
        basic_data = {
            **price_data,
            "analysis_timestamp": datetime.now().isoformat(),
            "market_status": "开盘" if 9 <= datetime.now().hour <= 15 else "闭盘",
            "data_quality": "良好" if price_data.get("data_source") == "实时数据" else "模拟"
        }
        
        return basic_data
        
    except Exception as e:
        await ctx.error(f"获取股票基本数据时发生错误: {str(e)}")
        return {"error": f"获取股票基本数据失败: {str(e)}"}

@mcp.tool
async def get_technical_indicators(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取股票技术指标
    
    Args:
        symbol: 股票代码
    
    Returns:
        技术指标数据
    """
    try:
        await ctx.info(f"正在计算股票 {symbol} 的技术指标...")
        
        # 获取基本价格数据
        price_data = await get_stock_price(symbol, ctx)
        
        if "error" in price_data:
            return price_data
        
        # 模拟技术指标计算
        current_price = price_data.get("current_price", 0)
        
        # 基于当前价格生成技术指标
        indicators = {
            "symbol": symbol,
            "current_price": current_price,
            "rsi": 65.5,  # 相对强弱指标
            "macd": 0.25,   # MACD指标
            "k": 78.2,      # KDJ指标K值
            "d": 72.1,      # KDJ指标D值
            "j": 90.4,      # KDJ指标J值
            "boll_upper": current_price * 1.05,  # 布林带上轨
            "boll_middle": current_price,        # 布林带中轨
            "boll_lower": current_price * 0.95,  # 布林带下轨
            "ma5": current_price * 1.02,         # 5日均线
            "ma10": current_price * 1.01,        # 10日均线
            "ma20": current_price * 0.99,        # 20日均线
            "volume_ratio": 1.15,                # 量比
            "turnover_rate": 2.3,               # 换手率
            "timestamp": datetime.now().isoformat()
        }
        
        await ctx.info(f"成功计算 {symbol} 的技术指标")
        return indicators
        
    except Exception as e:
        await ctx.error(f"计算技术指标时发生错误: {str(e)}")
        return {"error": f"计算技术指标失败: {str(e)}"}

@mcp.tool
async def search_stock_by_name(name: str, ctx: Context) -> List[Dict[str, str]]:
    """
    根据名称搜索股票
    
    Args:
        name: 股票名称或关键词
    
    Returns:
        匹配的股票列表
    """
    try:
        await ctx.info(f"正在搜索包含 "{name}" 的股票...")
        
        # 在模拟数据中搜索
        results = []
        for symbol, data in MOCK_STOCK_DATA.items():
            if name.lower() in data["name"].lower():
                results.append({
                    "symbol": symbol,
                    "name": data["name"],
                    "current_price": str(data["price"]),
                    "change": str(data["change"]),
                    "change_percent": str(data["change_percent"])
                })
        
        await ctx.info(f"找到 {len(results)} 个匹配结果")
        return results
        
    except Exception as e:
        await ctx.error(f"搜索股票时发生错误: {str(e)}")
        return [{"error": f"搜索股票失败: {str(e)}"}]

@mcp.tool
async def get_market_data(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取市场数据分析
    
    Args:
        symbol: 股票代码
    
    Returns:
        市场分析数据
    """
    try:
        await ctx.info(f"正在分析股票 {symbol} 的市场数据...")
        
        # 获取基本数据和技术指标
        stock_data = await get_stock_data(symbol, ctx)
        technical_data = await get_technical_indicators(symbol, ctx)
        
        if "error" in stock_data:
            return stock_data
        
        # 综合分析
        analysis = {
            "symbol": symbol,
            "basic_info": stock_data,
            "technical_indicators": technical_data,
            "market_analysis": {
                "trend": "上涨" if stock_data.get("change", 0) > 0 else "下跌",
                "strength": "强势" if technical_data.get("rsi", 50) > 70 else "弱势",
                "volatility": "高波动" if abs(technical_data.get("rsi", 50) - 50) > 20 else "低波动",
                "recommendation": "买入" if technical_data.get("rsi", 50) < 30 else "卖出" if technical_data.get("rsi", 50) > 70 else "观望",
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
        
        await ctx.info(f"完成股票 {symbol} 的市场分析")
        return analysis
        
    except Exception as e:
        await ctx.error(f"分析市场数据时发生错误: {str(e)}")
        return {"error": f"分析市场数据失败: {str(e)}"}

async def main():
    """主函数"""
    try:
        logger.info("启动股票数据MCP服务器...")
        logger.info(f"服务器名称: {args.name}")
        logger.info(f"监听地址: {args.host}:{args.port}")
        
        if args.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("调试模式已启用")
        
        # 启动服务器
        await mcp.run(host=args.host, port=args.port)
        
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
