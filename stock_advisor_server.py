"""
股票建议MCP服务器
提供股票分析、价格查询和投资建议功能
"""

import argparse
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP, Context
import aiohttp
import logging
from stock_data_fetcher import fetch_stock_data, search_stock, StockDataFetcher, get_historical_price
from technical_analysis import TechnicalAnalyzer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 解析命令行参数
parser = argparse.ArgumentParser(description="股票建议MCP服务器")
parser.add_argument("--name", type=str, default="股票建议助手", help="服务器名称")
parser.add_argument("--debug", action="store_true", help="启用调试模式")
parser.add_argument("--api-key", type=str, help="股票API密钥（如果需要）")
args = parser.parse_args()

# 创建MCP服务器实例
mcp = FastMCP(name=args.name)

# 模拟股票数据（实际使用时需要替换为真实API）
MOCK_STOCK_DATA = {
    "AAPL": {
        "name": "苹果公司",
        "price": 175.43,
        "change": 2.15,
        "change_percent": 1.24,
        "volume": 45678900,
        "market_cap": "2.8T",
        "pe_ratio": 28.5,
        "dividend_yield": 0.52
    },
    "GOOGL": {
        "name": "谷歌",
        "price": 142.56,
        "change": -1.23,
        "change_percent": -0.85,
        "volume": 23456789,
        "market_cap": "1.8T",
        "pe_ratio": 25.3,
        "dividend_yield": 0.0
    },
    "TSLA": {
        "name": "特斯拉",
        "price": 248.42,
        "change": 5.67,
        "change_percent": 2.34,
        "volume": 67890123,
        "market_cap": "790B",
        "pe_ratio": 65.2,
        "dividend_yield": 0.0
    },
    "MSFT": {
        "name": "微软",
        "price": 378.85,
        "change": 3.21,
        "change_percent": 0.85,
        "volume": 34567890,
        "market_cap": "2.8T",
        "pe_ratio": 32.1,
        "dividend_yield": 0.68
    },
    "600975": {
        "name": "新五丰",
        "price": 6.46,
        "change": -0.05,
        "change_percent": -0.77,
        "volume": 200743,
        "market_cap": "5.2B",
        "pe_ratio": 0.0,
        "dividend_yield": 0.0
    }
}

@mcp.tool
async def get_stock_price(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取指定股票的当前价格和基本信息
    支持A股股票代码（如 000001, 600036等）和美股代码（如 AAPL等）
    
    Args:
        symbol: 股票代码
    
    Returns:
        包含股票价格、涨跌幅、成交量等信息的字典
    """
    await ctx.info(f"正在从实时数据源查询股票 {symbol} 的价格信息...")
    
    try:
        # 首先尝试获取真实数据
        comprehensive_data = await fetch_stock_data(symbol)
        
        if comprehensive_data.get('basic_info'):
            basic_info = comprehensive_data['basic_info']
            result = {
                "symbol": symbol,
                "name": basic_info.get("name", ""),
                "current_price": basic_info.get("price", 0),
                "change": basic_info.get("change", 0),
                "change_percent": basic_info.get("change_percent", 0),
                "volume": basic_info.get("volume", 0),
                "turnover": basic_info.get("turnover", 0),
                "high": basic_info.get("high", 0),
                "low": basic_info.get("low", 0),
                "open": basic_info.get("open", 0),
                "pre_close": basic_info.get("pre_close", 0),
                "market_cap": basic_info.get("market_cap", 0),
                "pe_ratio": basic_info.get("pe_ratio", 0),
                "data_sources": comprehensive_data.get("data_sources", []),
                "timestamp": comprehensive_data.get("timestamp"),
                "has_news": len(comprehensive_data.get("news", [])) > 0
            }
            
            await ctx.info(f"成功从 {', '.join(comprehensive_data.get('data_sources', []))} 获取 {symbol} 的实时数据")
            return result
        else:
            # 如果获取真实数据失败，回退到模拟数据
            await ctx.info(f"无法获取 {symbol} 的实时数据，使用模拟数据")
            symbol_upper = symbol.upper()
            if symbol_upper in MOCK_STOCK_DATA:
                stock_data = MOCK_STOCK_DATA[symbol_upper]
                return {
                    "symbol": symbol,
                    "name": stock_data["name"],
                    "current_price": stock_data["price"],
                    "change": stock_data["change"],
                    "change_percent": stock_data["change_percent"],
                    "volume": stock_data["volume"],
                    "market_cap": stock_data["market_cap"],
                    "pe_ratio": stock_data["pe_ratio"],
                    "dividend_yield": stock_data["dividend_yield"],
                    "timestamp": datetime.now().isoformat(),
                    "data_source": "模拟数据"
                }
            else:
                return {"error": f"未找到股票代码 {symbol} 的数据"}
                
    except Exception as e:
        await ctx.error(f"获取股票数据时发生错误: {str(e)}")
        return {"error": f"获取股票数据失败: {str(e)}"}

@mcp.tool
async def get_professional_investment_advice(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取专业投资建议，包括基本面分析、情绪分析、资金流分析和技术指标分析
    
    Args:
        symbol: 股票代码
    
    Returns:
        专业投资建议报告
    """
    await ctx.info(f"正在生成股票 {symbol} 的专业投资建议...")
    
    try:
        async with StockDataFetcher() as fetcher:
            # 获取基础数据
            await ctx.info(f"获取 {symbol} 基础数据...")
            basic_info = await fetcher.get_stock_info_from_eastmoney(symbol)
            if not basic_info:
                await ctx.error(f"无法获取股票 {symbol} 的基础数据")
                return {"error": f"无法获取股票 {symbol} 的基础数据"}
            
            await ctx.info(f"成功获取基础数据: {basic_info.get('name', 'N/A')}")
            
            # 获取专业分析数据
            await ctx.info("获取专业分析数据...")
            
            # 逐个获取数据，避免并发问题
            financial_data = None
            money_flow = None
            tech_indicators = None
            sentiment = None
            news = None
            
            try:
                financial_data = await fetcher.get_stock_financial_data(symbol)
                await ctx.info("财务数据获取完成")
            except Exception as e:
                await ctx.error(f"财务数据获取失败: {e}")
                financial_data = {}
            
            try:
                money_flow = await fetcher.get_money_flow_data(symbol)
                await ctx.info("资金流数据获取完成")
            except Exception as e:
                await ctx.error(f"资金流数据获取失败: {e}")
                money_flow = {}
            
            try:
                tech_indicators = await fetcher.get_technical_indicators(symbol)
                await ctx.info("技术指标数据获取完成")
            except Exception as e:
                await ctx.error(f"技术指标数据获取失败: {e}")
                tech_indicators = {}
            
            try:
                sentiment = await fetcher.get_market_sentiment(symbol)
                await ctx.info("市场情绪数据获取完成")
            except Exception as e:
                await ctx.error(f"市场情绪数据获取失败: {e}")
                sentiment = {}
            
            try:
                news = await fetcher.get_stock_news(symbol)
                await ctx.info("新闻数据获取完成")
            except Exception as e:
                await ctx.error(f"新闻数据获取失败: {e}")
                news = []
            
            # 构建综合分析报告
            analysis_report = {
                "symbol": symbol,
                "name": basic_info.get("name", ""),
                "current_price": basic_info.get("price", 0),
                "analysis_timestamp": datetime.now().isoformat(),
                "data_sources": ["eastmoney", "financial", "news"],
                "basic_info": basic_info,
                "technical_analysis": tech_indicators,
                "fundamental_analysis": financial_data,
                "money_flow_analysis": money_flow,
                "market_sentiment": sentiment,
                "recent_news": news[:5]  # 只保留最近5条新闻
            }
            
            # 生成投资建议
            recommendation = await _generate_investment_recommendation(analysis_report, ctx)
            
            return recommendation
            
    except Exception as e:
        await ctx.error(f"生成投资建议时发生错误: {str(e)}")
        return {"error": f"生成投资建议失败: {str(e)}"}

@mcp.tool
async def search_stock_by_name(name: str, ctx: Context) -> List[Dict[str, Any]]:
    """
    根据股票名称搜索股票代码
    
    Args:
        name: 股票名称或关键词
    
    Returns:
        匹配的股票列表
    """
    await ctx.info(f"正在搜索包含 '{name}' 的股票...")
    
    try:
        results = await search_stock(name)
        if results:
            await ctx.info(f"找到 {len(results)} 个匹配的股票")
            return results
        else:
            await ctx.info("未找到匹配的股票")
            return [{"message": f"未找到包含 '{name}' 的股票"}]
            
    except Exception as e:
        await ctx.error(f"搜索股票时发生错误: {str(e)}")
        return [{"error": f"搜索失败: {str(e)}"}]

@mcp.tool
async def get_comprehensive_analysis(symbol: str, ctx: Context) -> Dict[str, Any]:
    """
    获取股票的完整综合分析报告
    
    Args:
        symbol: 股票代码
    
    Returns:
        包含所有分析维度的完整报告
    """
    await ctx.info(f"正在生成股票 {symbol} 的完整综合分析报告...")
    
    try:
        # 获取基础价格信息
        price_info = await get_stock_price(symbol, ctx)
        if "error" in price_info:
            return price_info
        
        # 获取专业投资建议
        investment_advice = await get_professional_investment_advice(symbol, ctx)
        if "error" in investment_advice:
            return investment_advice
        
        # 合并所有信息
        comprehensive_report = {
            "symbol": symbol,
            "name": price_info.get("name", ""),
            "analysis_date": datetime.now().isoformat(),
            "price_info": price_info,
            "investment_advice": investment_advice,
            "summary": {
                "current_price": price_info.get("current_price", 0),
                "recommendation": investment_advice.get("recommendation", "未知"),
                "confidence": investment_advice.get("confidence", 0),
                "target_price": investment_advice.get("target_price", 0),
                "stop_loss": investment_advice.get("stop_loss", 0),
                "risk_level": investment_advice.get("risk_level", "未知")
            }
        }
        
        return comprehensive_report
        
    except Exception as e:
        await ctx.error(f"生成综合分析报告时发生错误: {str(e)}")
        return {"error": f"生成综合分析报告失败: {str(e)}"}

async def _generate_investment_recommendation(analysis_report: Dict[str, Any], ctx: Context) -> Dict[str, Any]:
    """生成投资建议"""
    try:
        symbol = analysis_report["symbol"]
        name = analysis_report["name"]
        current_price = analysis_report["current_price"]
        
        # 计算各维度评分
        fundamental_score = await _analyze_fundamentals(analysis_report, ctx)
        technical_score = await _analyze_technical_indicators(analysis_report, ctx)
        money_flow_score = await _analyze_money_flow(analysis_report, ctx)
        sentiment_score = await _analyze_market_sentiment(analysis_report, ctx)
        
        # 计算综合评分
        weights = {
            "fundamental": 0.30,
            "technical": 0.30,
            "money_flow": 0.25,
            "sentiment": 0.15
        }
        
        overall_score = (
            fundamental_score * weights["fundamental"] +
            technical_score * weights["technical"] +
            money_flow_score * weights["money_flow"] +
            sentiment_score * weights["sentiment"]
        )
        
        # 生成投资建议
        recommendation = await _generate_final_recommendation(
            overall_score, current_price, ctx
        )
        
        return {
            "symbol": symbol,
            "name": name,
            "current_price": current_price,
            "analysis": {
                "fundamental_analysis": {
                    "score": fundamental_score,
                    "assessment": _get_score_assessment(fundamental_score)
                },
                "technical_analysis": {
                    "score": technical_score,
                    "assessment": _get_score_assessment(technical_score)
                },
                "money_flow_analysis": {
                    "score": money_flow_score,
                    "assessment": _get_score_assessment(money_flow_score)
                },
                "market_sentiment": {
                    "score": sentiment_score,
                    "assessment": _get_score_assessment(sentiment_score)
                }
            },
            "overall_score": round(overall_score, 1),
            "recommendation": recommendation["recommendation"],
            "confidence": recommendation["confidence"],
            "target_price": recommendation["target_price"],
            "stop_loss": recommendation["stop_loss"],
            "risk_level": recommendation["risk_level"],
            "reasoning": recommendation["reasoning"],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        await ctx.error(f"生成投资建议时发生错误: {str(e)}")
        return {"error": f"生成投资建议失败: {str(e)}"}

async def _analyze_fundamentals(analysis_report: Dict[str, Any], ctx: Context) -> float:
    """分析基本面"""
    try:
        score = 50  # 基础分
        
        basic_info = analysis_report.get("basic_info", {})
        financial_data = analysis_report.get("fundamental_analysis", {})
        
        # PE估值评估
        pe_ratio = basic_info.get("pe_ratio", 0)
        if pe_ratio > 0:
            if pe_ratio < 15:
                score += 15  # 低估值
            elif pe_ratio < 25:
                score += 10  # 合理估值
            elif pe_ratio < 40:
                score += 5   # 略高估值
            else:
                score -= 5   # 高估值
        
        # 市值稳定性
        market_cap = basic_info.get("market_cap", 0)
        if market_cap > 100000000000:  # 1000亿以上
            score += 10
        elif market_cap > 50000000000:  # 500亿以上
            score += 5
        
        return min(100, max(0, score))
        
    except Exception as e:
        await ctx.error(f"基本面分析失败: {str(e)}")
        return 50

async def _analyze_technical_indicators(analysis_report: Dict[str, Any], ctx: Context) -> float:
    """分析技术指标"""
    try:
        score = 50  # 基础分
        
        basic_info = analysis_report.get("basic_info", {})
        tech_data = analysis_report.get("technical_analysis", {})
        
        # 价格趋势分析
        change_percent = basic_info.get("change_percent", 0)
        if change_percent > 5:
            score += 15
        elif change_percent > 2:
            score += 10
        elif change_percent > 0:
            score += 5
        elif change_percent < -5:
            score -= 15
        elif change_percent < -2:
            score -= 10
        
        # 成交量分析
        volume = basic_info.get("volume", 0)
        if volume > 1000000:  # 高成交量
            score += 5
        
        return min(100, max(0, score))
        
    except Exception as e:
        await ctx.error(f"技术面分析失败: {str(e)}")
        return 50

async def _analyze_money_flow(analysis_report: Dict[str, Any], ctx: Context) -> float:
    """分析资金流向"""
    try:
        score = 50  # 基础分
        
        money_flow_data = analysis_report.get("money_flow_analysis", {})
        
        # 主力资金流向
        main_inflow = money_flow_data.get("main_net_inflow", 0)
        if main_inflow > 10000000:  # 1000万以上流入
            score += 20
        elif main_inflow > 5000000:  # 500万以上流入
            score += 15
        elif main_inflow > 1000000:  # 100万以上流入
            score += 10
        elif main_inflow < -10000000:  # 1000万以上流出
            score -= 20
        elif main_inflow < -5000000:  # 500万以上流出
            score -= 15
        
        return min(100, max(0, score))
        
    except Exception as e:
        await ctx.error(f"资金流向分析失败: {str(e)}")
        return 50

async def _analyze_market_sentiment(analysis_report: Dict[str, Any], ctx: Context) -> float:
    """分析市场情绪"""
    try:
        score = 50  # 基础分
        
        sentiment_data = analysis_report.get("market_sentiment", {})
        news_list = analysis_report.get("recent_news", [])
        
        # 新闻数量评估
        news_count = len(news_list)
        if news_count >= 5:
            score += 10  # 高关注度
        elif news_count >= 3:
            score += 5   # 中等关注度
        
        # 新闻情绪分析（简单实现）
        positive_keywords = ["增长", "预增", "盈利", "利好", "上涨"]
        negative_keywords = ["下跌", "亏损", "减持", "利空", "风险"]
        
        positive_count = 0
        negative_count = 0
        
        for news in news_list:
            title = news.get("title", "")
            content = news.get("summary", "")
            text = title + content
            
            for keyword in positive_keywords:
                if keyword in text:
                    positive_count += 1
            
            for keyword in negative_keywords:
                if keyword in text:
                    negative_count += 1
        
        # 情绪评分
        if positive_count > negative_count:
            score += 15
        elif positive_count == negative_count and positive_count > 0:
            score += 5
        elif negative_count > positive_count:
            score -= 10
        
        return min(100, max(0, score))
        
    except Exception as e:
        await ctx.error(f"市场情绪分析失败: {str(e)}")
        return 50

async def _generate_final_recommendation(score: float, current_price: float, ctx: Context) -> Dict[str, Any]:
    """生成最终投资建议"""
    try:
        # 根据评分生成建议
        if score >= 75:
            recommendation = "强烈推荐"
            confidence = "高"
            target_gain = 0.15  # 15%目标涨幅
            stop_loss_percent = 0.08  # 8%止损
        elif score >= 65:
            recommendation = "推荐"
            confidence = "较高"
            target_gain = 0.10  # 10%目标涨幅
            stop_loss_percent = 0.06  # 6%止损
        elif score >= 55:
            recommendation = "谨慎关注"
            confidence = "中等"
            target_gain = 0.05  # 5%目标涨幅
            stop_loss_percent = 0.04  # 4%止损
        elif score >= 45:
            recommendation = "观望"
            confidence = "中等"
            target_gain = 0.02  # 2%目标涨幅
            stop_loss_percent = 0.02  # 2%止损
        else:
            recommendation = "回避"
            confidence = "高"
            target_gain = -0.02  # -2%预期跌幅
            stop_loss_percent = 0.05  # 5%止损
        
        target_price = round(current_price * (1 + target_gain), 2)
        stop_loss_price = round(current_price * (1 - stop_loss_percent), 2)
        
        # 风险等级
        if score >= 75:
            risk_level = "低"
        elif score >= 55:
            risk_level = "中"
        else:
            risk_level = "高"
        
        # 投资建议理由
        reasoning = f"基于综合评分{score:.1f}分，{recommendation}该股票"
        
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "target_price": target_price,
            "stop_loss": stop_loss_price,
            "risk_level": risk_level,
            "reasoning": reasoning
        }
        
    except Exception as e:
        await ctx.error(f"生成最终投资建议失败: {str(e)}")
        return {
            "recommendation": "未知",
            "confidence": "低",
            "target_price": current_price,
            "stop_loss": current_price * 0.9,
            "risk_level": "高",
            "reasoning": "分析过程中发生错误"
        }

def _get_score_assessment(score: float) -> str:
    """根据分数返回评估描述"""
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 70:
        return "较好"
    elif score >= 60:
        return "一般"
    elif score >= 50:
        return "较弱"
    else:
        return "较差"

if __name__ == "__main__":
    print("🚀 启动股票建议MCP服务器...")
    print(f"服务器名称: {args.name}")
    if args.debug:
        print("🐛 调试模式已启用")
    
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")