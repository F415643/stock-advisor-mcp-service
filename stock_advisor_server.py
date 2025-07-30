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
                await ctx.info("技术指标获取完成")
            except Exception as e:
                await ctx.error(f"技术指标获取失败: {e}")
                tech_indicators = {}
            
            try:
                sentiment = await fetcher.get_market_sentiment(symbol)
                await ctx.info("市场情绪获取完成")
            except Exception as e:
                await ctx.error(f"市场情绪获取失败: {e}")
                sentiment = {}
            
            try:
                news = await fetcher.get_stock_news(symbol)
                await ctx.info(f"新闻数据获取完成，共{len(news) if news else 0}条")
            except Exception as e:
                await ctx.error(f"新闻数据获取失败: {e}")
                news = []
            
            # 生成专业投资建议
            await ctx.info("开始生成专业投资建议...")
            advice = await _generate_professional_advice(
                basic_info, financial_data, money_flow, tech_indicators, sentiment, news, ctx
            )
            
            await ctx.info(f"成功生成 {symbol} 的专业投资建议")
            return advice
            
    except Exception as e:
        await ctx.error(f"生成专业投资建议时发生错误: {str(e)}")
        import traceback
        await ctx.error(f"错误详情: {traceback.format_exc()}")
        return {"error": f"生成专业投资建议失败: {str(e)}"}

async def _generate_professional_advice(basic_info: Dict, financial_data: Dict, money_flow: Dict, 
                                      tech_indicators: Dict, sentiment: Dict, news: List, ctx: Context) -> Dict[str, Any]:
    """生成专业投资建议"""
    
    # 安全获取数据
    symbol = basic_info.get('symbol', '') if isinstance(basic_info, dict) else ''
    current_price = basic_info.get('price', 0) if isinstance(basic_info, dict) else 0
    change_percent = basic_info.get('change_percent', 0) if isinstance(basic_info, dict) else 0
    
    await ctx.info(f"开始分析 {symbol} 的专业投资建议...")
    
    # 1. 基本面分析
    try:
        fundamental_score = _analyze_fundamentals(basic_info, financial_data)
        await ctx.info(f"基本面分析完成，评分: {fundamental_score}")
    except Exception as e:
        await ctx.error(f"基本面分析失败: {e}")
        fundamental_score = 50
    
    # 2. 技术面分析
    try:
        technical_score = _analyze_technical_indicators(tech_indicators, basic_info)
        await ctx.info(f"技术面分析完成，评分: {technical_score}")
    except Exception as e:
        await ctx.error(f"技术面分析失败: {e}")
        technical_score = 50
    
    # 3. 资金流分析
    try:
        money_flow_score = _analyze_money_flow(money_flow, basic_info)
        await ctx.info(f"资金流分析完成，评分: {money_flow_score}")
    except Exception as e:
        await ctx.error(f"资金流分析失败: {e}")
        money_flow_score = 50
    
    # 4. 情绪分析
    try:
        sentiment_score = _analyze_market_sentiment(sentiment, news)
        await ctx.info(f"情绪分析完成，评分: {sentiment_score}")
    except Exception as e:
        await ctx.error(f"情绪分析失败: {e}")
        sentiment_score = 50
    
    # 5. 综合评分
    total_score = (fundamental_score * 0.3 + technical_score * 0.3 + 
                  money_flow_score * 0.25 + sentiment_score * 0.15)
    
    await ctx.info(f"综合评分计算完成: {total_score:.2f}")
    
    # 6. 生成投资建议
    try:
        investment_advice = _generate_final_recommendation(total_score, {
            'fundamental': fundamental_score,
            'technical': technical_score, 
            'money_flow': money_flow_score,
            'sentiment': sentiment_score
        })
        await ctx.info("投资建议生成完成")
    except Exception as e:
        await ctx.error(f"投资建议生成失败: {e}")
        investment_advice = {
            'recommendation': '观望',
            'confidence': '中等',
            'target_multiplier': 1.02,
            'stop_loss_multiplier': 0.98,
            'position_size': '空仓',
            'time_horizon': '观望',
            'reasons': ['数据分析异常'],
            'risks': ['建议等待系统恢复正常']
        }
    
    return {
        "symbol": symbol,
        "current_price": current_price,
        "change_percent": change_percent,
        "analysis_timestamp": datetime.now().isoformat(),
        
        # 详细分析
        "fundamental_analysis": {
            "score": fundamental_score,
            "pe_ratio": basic_info.get('pe_ratio', 0),
            "market_cap": basic_info.get('market_cap', 0),
            "financial_health": "良好" if financial_data and isinstance(financial_data, dict) else "数据不足",
            "assessment": _get_fundamental_assessment(fundamental_score)
        },
        
        "technical_analysis": {
            "score": technical_score,
            "indicators": tech_indicators if isinstance(tech_indicators, dict) else {},
            "trend": "上涨" if change_percent > 0 else "下跌" if change_percent < 0 else "横盘",
            "assessment": _get_technical_assessment(technical_score)
        },
        
        "money_flow_analysis": {
            "score": money_flow_score,
            "main_net_inflow": money_flow.get('main_net_inflow', 0) if isinstance(money_flow, dict) else 0,
            "volume_ratio": tech_indicators.get('volume_ratio', 0) if isinstance(tech_indicators, dict) else 0,
            "assessment": _get_money_flow_assessment(money_flow_score)
        },
        
        "sentiment_analysis": {
            "score": sentiment_score,
            "news_count": len(news) if isinstance(news, list) else 0,
            "market_attention": sentiment.get('market_attention', 'medium') if isinstance(sentiment, dict) else 'medium',
            "assessment": _get_sentiment_assessment(sentiment_score)
        },
        
        # 综合建议
        "investment_recommendation": {
            "total_score": round(total_score, 2),
            "recommendation": investment_advice['recommendation'],
            "confidence_level": investment_advice['confidence'],
            "target_price": round(current_price * investment_advice['target_multiplier'], 2),
            "stop_loss": round(current_price * investment_advice['stop_loss_multiplier'], 2),
            "position_size": investment_advice['position_size'],
            "time_horizon": investment_advice['time_horizon'],
            "key_reasons": investment_advice['reasons'],
            "risk_warnings": investment_advice['risks']
        }
    }

def _analyze_fundamentals(basic_info: Dict, financial_data: Dict) -> float:
    """基本面分析评分 (0-100)"""
    score = 50  # 基础分
    
    try:
        pe_ratio = basic_info.get('pe_ratio', 0)
        market_cap = basic_info.get('market_cap', 0)
        
        # PE估值分析
        if 0 < pe_ratio < 15:
            score += 20  # 低估值
        elif 15 <= pe_ratio < 25:
            score += 10  # 合理估值
        elif pe_ratio >= 40:
            score -= 15  # 高估值
        
        # 市值稳定性
        if market_cap > 50000000000:  # 500亿以上
            score += 10
        elif market_cap > 10000000000:  # 100亿以上
            score += 5
        
        # 财务数据分析
        if isinstance(financial_data, dict) and financial_data:
            if financial_data.get('roe'):
                score += 10  # 有ROE数据
            if financial_data.get('profit'):
                score += 5   # 有利润数据
    
    except Exception:
        pass
    
    return max(0, min(100, score))

def _analyze_technical_indicators(tech_indicators: Dict, basic_info: Dict) -> float:
    """技术指标分析评分 (0-100)"""
    score = 50  # 基础分
    
    try:
        if not isinstance(tech_indicators, dict):
            return score
        
        current_price = basic_info.get('price', 0)
        
        # 移动平均线分析
        ma5 = tech_indicators.get('ma5', 0)
        ma10 = tech_indicators.get('ma10', 0)
        ma20 = tech_indicators.get('ma20', 0)
        
        if ma5 > 0 and ma10 > 0 and ma20 > 0:
            if current_price > ma5 > ma10 > ma20:
                score += 20  # 多头排列
            elif current_price > ma5 > ma10:
                score += 10  # 短期向好
            elif current_price < ma5 < ma10 < ma20:
                score -= 20  # 空头排列
        
        # RSI分析
        rsi = tech_indicators.get('rsi', 50)
        if 30 <= rsi <= 70:
            score += 10  # RSI正常区间
        elif rsi < 30:
            score += 15  # 超卖，可能反弹
        elif rsi > 70:
            score -= 10  # 超买，注意风险
        
        # MFI分析
        mfi = tech_indicators.get('mfi', 50)
        if 20 <= mfi <= 80:
            score += 5   # MFI正常
        elif mfi < 20:
            score += 10  # 资金超卖
        elif mfi > 80:
            score -= 10  # 资金超买
        
    except Exception:
        pass
    
    return max(0, min(100, score))

def _analyze_money_flow(money_flow: Dict) -> float:
    """资金流分析评分 (0-100)"""
    score = 50  # 基础分
    
    try:
        if not isinstance(money_flow, dict):
            return score
        
        main_net_inflow = money_flow.get('main_net_inflow', 0)
        super_large_net = money_flow.get('super_large_net', 0)
        large_net = money_flow.get('large_net', 0)
        
        # 主力资金流入分析
        if main_net_inflow > 0:
            score += 20  # 主力净流入
            if main_net_inflow > 10000000:  # 1000万以上
                score += 10
        else:
            score -= 15  # 主力净流出
        
        # 超大单分析
        if super_large_net > 0:
            score += 15  # 超大单净流入
        elif super_large_net < -5000000:  # 500万以上流出
            score -= 10
        
        # 大单分析
        if large_net > 0:
            score += 10  # 大单净流入
        
    except Exception:
        pass
    
    return max(0, min(100, score))

def _analyze_market_sentiment(sentiment: Dict, news: List) -> float:
    """市场情绪分析评分 (0-100)"""
    score = 50  # 基础分
    
    try:
        # 新闻数量分析
        if isinstance(news, list):
            news_count = len(news)
            if news_count > 5:
                score += 10  # 关注度高
            elif news_count > 2:
                score += 5   # 关注度中等
        
        # 市场关注度
        if isinstance(sentiment, dict):
            attention = sentiment.get('market_attention', 'medium')
            if attention == 'high':
                score += 15
            elif attention == 'low':
                score -= 5
        
    except Exception:
        pass
    
    return max(0, min(100, score))

def _generate_final_recommendation(total_score: float, scores: Dict) -> Dict[str, Any]:
    """生成最终投资建议"""
    
    if total_score >= 75:
        recommendation = "强烈推荐"
        confidence = "高"
        target_multiplier = 1.15
        stop_loss_multiplier = 0.92
        position_size = "重仓"
        time_horizon = "中长期"
        reasons = ["基本面优秀", "技术面强势", "资金流入积极"]
        risks = ["注意大盘系统性风险"]
    elif total_score >= 65:
        recommendation = "推荐"
        confidence = "较高"
        target_multiplier = 1.10
        stop_loss_multiplier = 0.94
        position_size = "标准仓位"
        time_horizon = "中期"
        reasons = ["综合表现良好", "上涨概率较大"]
        risks = ["关注技术面变化", "控制仓位风险"]
    elif total_score >= 55:
        recommendation = "谨慎关注"
        confidence = "中等"
        target_multiplier = 1.05
        stop_loss_multiplier = 0.96
        position_size = "轻仓"
        time_horizon = "短期"
        reasons = ["存在一定机会"]
        risks = ["不确定性较大", "建议小仓位试探"]
    elif total_score >= 45:
        recommendation = "观望"
        confidence = "中等"
        target_multiplier = 1.02
        stop_loss_multiplier = 0.98
        position_size = "空仓"
        time_horizon = "观望"
        reasons = ["等待更好时机"]
        risks = ["当前风险收益比不佳"]
    else:
        recommendation = "回避"
        confidence = "低"
        target_multiplier = 0.98
        stop_loss_multiplier = 0.95
        position_size = "空仓"
        time_horizon = "回避"
        reasons = ["风险较大"]
        risks = ["建议等待更好机会"]
    
    return {
        'recommendation': recommendation,
        'confidence': confidence,
        'target_multiplier': target_multiplier,
        'stop_loss_multiplier': stop_loss_multiplier,
        'position_size': position_size,
        'time_horizon': time_horizon,
        'reasons': reasons,
        'risks': risks
    }

if __name__ == "__main__":
    mcp.run()