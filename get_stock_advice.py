"""
股票投资建议生成模块
基于多维度分析提供专业投资建议
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

from stock_data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockAdvisor:
    """股票投资建议生成器"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.tech_analyzer = TechnicalAnalyzer()
        
    async def get_professional_advice(self, symbol: str) -> Dict[str, Any]:
        """获取专业投资建议"""
        try:
            # 获取股票综合数据
            stock_data = await self.data_fetcher.fetch_stock_data(symbol)
            
            if "error" in stock_data:
                return {"error": stock_data["error"]}
            
            # 生成投资建议
            advice = await self.generate_investment_advice(stock_data)
            
            # 计算风险等级
            risk_level = self.calculate_risk_level(stock_data)
            
            # 生成买卖信号
            trading_signals = self.generate_trading_signals(stock_data)
            
            # 计算目标价位
            target_prices = self.calculate_target_prices(stock_data)
            
            return {
                "symbol": symbol,
                "advice_date": datetime.now().isoformat(),
                "current_price": stock_data.get("basic_info", {}).get("price", 0),
                "advice": advice,
                "risk_level": risk_level,
                "trading_signals": trading_signals,
                "target_prices": target_prices,
                "key_metrics": self.extract_key_metrics(stock_data),
                "market_outlook": self.analyze_market_outlook(stock_data),
                "recommendations": self.generate_recommendations(stock_data, risk_level)
            }
            
        except Exception as e:
            logger.error(f"生成投资建议失败: {e}")
            return {"error": str(e)}
    
    async def generate_investment_advice(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成投资建议"""
        basic_info = stock_data.get("basic_info", {})
        technical = stock_data.get("technical_indicators", {})
        financial = stock_data.get("financial_data", {})
        money_flow = stock_data.get("money_flow", {})
        sentiment = stock_data.get("sentiment", {})
        
        # 基础评分
        fundamental_score = self.calculate_fundamental_score(basic_info, financial)
        technical_score = self.calculate_technical_score(technical)
        sentiment_score = self.calculate_sentiment_score(sentiment, money_flow)
        
        # 综合评分
        total_score = (fundamental_score * 0.4 + technical_score * 0.35 + sentiment_score * 0.25)
        
        # 投资建议
        if total_score >= 80:
            recommendation = "强烈推荐"
            action = "买入"
            confidence = "高"
        elif total_score >= 65:
            recommendation = "推荐"
            action = "买入"
            confidence = "中高"
        elif total_score >= 50:
            recommendation = "中性"
            action = "持有"
            confidence = "中"
        elif total_score >= 35:
            recommendation = "谨慎"
            action = "减仓"
            confidence = "中低"
        else:
            recommendation = "卖出"
            action = "卖出"
            confidence = "低"
        
        return {
            "recommendation": recommendation,
            "action": action,
            "confidence": confidence,
            "score": total_score,
            "scores": {
                "fundamental": fundamental_score,
                "technical": technical_score,
                "sentiment": sentiment_score
            },
            "reasoning": self.generate_reasoning(stock_data, total_score)
        }
    
    def calculate_fundamental_score(self, basic_info: Dict, financial: Dict) -> float:
        """计算基本面评分"""
        score = 50  # 基础分
        
        # 估值指标
        pe_ratio = basic_info.get("pe_ratio", 0)
        pb_ratio = basic_info.get("pb_ratio", 0)
        
        if 0 < pe_ratio < 20:
            score += 15
        elif 20 <= pe_ratio < 30:
            score += 10
        elif pe_ratio >= 50 or pe_ratio < 0:
            score -= 20
        
        if 0 < pb_ratio < 2:
            score += 10
        elif pb_ratio >= 5:
            score -= 15
        
        # 财务指标
        roe = financial.get("roe", 0)
        profit_margin = financial.get("profit_margin", 0)
        debt_ratio = financial.get("debt_ratio", 0)
        
        if roe > 15:
            score += 10
        elif roe > 10:
            score += 5
        
        if profit_margin > 15:
            score += 10
        elif profit_margin > 10:
            score += 5
        
        if debt_ratio < 30:
            score += 5
        elif debt_ratio > 70:
            score -= 10
        
        return max(0, min(100, score))
    
    def calculate_technical_score(self, technical: Dict) -> float:
        """计算技术面评分"""
        score = 50  # 基础分
        
        # RSI指标
        rsi = technical.get("rsi", 50)
        if rsi < 30:
            score += 15
        elif rsi > 70:
            score -= 15
        elif 30 <= rsi <= 70:
            score += 5
        
        # MACD指标
        macd = technical.get("macd", {})
        if isinstance(macd, dict):
            macd_value = macd.get("macd", 0)
            signal = macd.get("signal", 0)
            
            if macd_value > signal and macd_value > 0:
                score += 10
            elif macd_value < signal and macd_value < 0:
                score -= 10
        
        # 移动平均线
        ma5 = technical.get("ma5", 0)
        ma20 = technical.get("ma20", 0)
        current_price = technical.get("current_price", 0)
        
        if current_price > ma5 > ma20:
            score += 10
        elif current_price < ma5 < ma20:
            score -= 10
        
        return max(0, min(100, score))
    
    def calculate_sentiment_score(self, sentiment: Dict, money_flow: Dict) -> float:
        """计算情绪评分"""
        score = 50  # 基础分
        
        # 资金流向
        main_net_inflow = money_flow.get("main_net_inflow", 0)
        if main_net_inflow > 0:
            score += 15
        elif main_net_inflow < 0:
            score -= 15
        
        # 市场情绪
        news_sentiment = sentiment.get("news_sentiment", 0.5)
        social_sentiment = sentiment.get("social_sentiment", 0.5)
        
        score += (news_sentiment - 0.5) * 30
        score += (social_sentiment - 0.5) * 20
        
        # 分析师评级
        analyst_rating = sentiment.get("analyst_rating", "hold")
        if analyst_rating == "buy":
            score += 10
        elif analyst_rating == "sell":
            score -= 10
        
        return max(0, min(100, score))
    
    def calculate_risk_level(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算风险等级"""
        basic_info = stock_data.get("basic_info", {})
        technical = stock_data.get("technical_indicators", {})
        
        # 波动率风险
        volatility = abs(technical.get("rsi", 50) - 50) / 50 * 100
        
        # 估值风险
        pe_ratio = basic_info.get("pe_ratio", 0)
        pe_risk = min(100, max(0, (pe_ratio - 20) * 2)) if pe_ratio > 0 else 50
        
        # 流动性风险
        volume = basic_info.get("volume", 0)
        volume_risk = max(0, 100 - min(100, volume / 1000000 * 10))
        
        # 综合风险
        total_risk = (volatility * 0.4 + pe_risk * 0.3 + volume_risk * 0.3)
        
        if total_risk < 30:
            risk_level = "低风险"
            risk_color = "绿色"
        elif total_risk < 60:
            risk_level = "中风险"
            risk_color = "黄色"
        else:
            risk_level = "高风险"
            risk_color = "红色"
        
        return {
            "risk_level": risk_level,
            "risk_color": risk_color,
            "risk_score": total_risk,
            "risk_factors": {
                "volatility_risk": volatility,
                "valuation_risk": pe_risk,
                "liquidity_risk": volume_risk
            }
        }
    
    def generate_trading_signals(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成交易信号"""
        technical = stock_data.get("technical_indicators", {})
        sentiment = stock_data.get("sentiment", {})
        
        signals = {}
        
        # RSI信号
        rsi = technical.get("rsi", 50)
        if rsi < 30:
            signals["rsi_signal"] = "超卖，可能反弹"
            signals["rsi_action"] = "考虑买入"
        elif rsi > 70:
            signals["rsi_signal"] = "超买，可能回调"
            signals["rsi_action"] = "考虑卖出"
        else:
            signals["rsi_signal"] = "正常区间"
            signals["rsi_action"] = "观望"
        
        # MACD信号
        macd = technical.get("macd", {})
        if isinstance(macd, dict):
            macd_value = macd.get("macd", 0)
            signal = macd.get("signal", 0)
            
            if macd_value > signal:
                signals["macd_signal"] = "金叉信号"
                signals["macd_action"] = "买入信号"
            else:
                signals["macd_signal"] = "死叉信号"
                signals["macd_action"] = "卖出信号"
        
        # 资金流向信号
        money_flow = stock_data.get("money_flow", {})
        main_net = money_flow.get("main_net_inflow", 0)
        if main_net > 0:
            signals["money_flow_signal"] = "主力资金流入"
            signals["money_flow_action"] = "看多"
        else:
            signals["money_flow_signal"] = "主力资金流出"
            signals["money_flow_action"] = "看空"
        
        return signals
    
    def calculate_target_prices(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算目标价位"""
        current_price = stock_data.get("basic_info", {}).get("price", 0)
        
        # 基于技术分析计算目标价
        technical = stock_data.get("technical_indicators", {})
        ma20 = technical.get("ma20", current_price)
        
        # 支撑位和阻力位
        support_price = current_price * 0.92  # 8%下跌空间
        resistance_price = current_price * 1.15  # 15%上涨空间
        
        # 基于波动率调整
        volatility = abs(technical.get("rsi", 50) - 50) / 50
        adjusted_support = support_price * (1 - volatility * 0.1)
        adjusted_resistance = resistance_price * (1 + volatility * 0.1)
        
        return {
            "current_price": current_price,
            "support_price": round(adjusted_support, 2),
            "resistance_price": round(adjusted_resistance, 2),
            "target_price_1m": round(current_price * 1.1, 2),
            "target_price_3m": round(current_price * 1.25, 2),
            "stop_loss": round(adjusted_support * 0.95, 2)
        }
    
    def extract_key_metrics(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取关键指标"""
        basic = stock_data.get("basic_info", {})
        financial = stock_data.get("financial_data", {})
        
        return {
            "估值指标": {
                "市盈率": f"{basic.get('pe_ratio', 0):.2f}",
                "市净率": f"{basic.get('pb_ratio', 0):.2f}",
                "股息率": f"{basic.get('dividend_yield', 0):.2f}%"
            },
            "财务指标": {
                "净资产收益率": f"{financial.get('roe', 0):.2f}%",
                "利润率": f"{financial.get('profit_margin', 0):.2f}%",
                "负债率": f"{financial.get('debt_ratio', 0):.2f}%"
            },
            "市场指标": {
                "成交量": f"{basic.get('volume', 0):,}",
                "市值": f"{basic.get('market_cap', 0):,.0f}元"
            }
        }
    
    def analyze_market_outlook(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析市场前景"""
        sentiment = stock_data.get("sentiment", {})
        news = stock_data.get("news", [])
        
        # 基于新闻和情绪分析
        positive_news = sum(1 for n in news if n.get("sentiment") == "positive")
        negative_news = sum(1 for n in news if n.get("sentiment") == "negative")
        
        news_sentiment_score = (positive_news - negative_news) / max(1, len(news))
        
        # 市场情绪
        social_sentiment = sentiment.get("social_sentiment", 0.5)
        analyst_rating = sentiment.get("analyst_rating", "hold")
        
        # 综合市场前景
        outlook_score = (news_sentiment_score + social_sentiment) / 2
        
        if outlook_score > 0.7:
            outlook = "非常乐观"
            trend = "上涨"
        elif outlook_score > 0.5:
            outlook = "乐观"
            trend = "温和上涨"
        elif outlook_score > 0.3:
            outlook = "中性"
            trend = "震荡"
        else:
            outlook = "谨慎"
            trend = "可能下跌"
        
        return {
            "market_outlook": outlook,
            "price_trend": trend,
            "sentiment_score": outlook_score,
            "analyst_consensus": analyst_rating,
            "key_drivers": [
                "行业基本面改善",
                "政策利好预期",
                "资金持续流入",
                "技术面转强"
            ]
        }
    
    def generate_recommendations(self, stock_data: Dict[str, Any], risk_level: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成具体建议"""
        risk_score = risk_level.get("risk_score", 50)
        
        recommendations = []
        
        # 基于风险等级的建议
        if risk_score < 30:
            recommendations.extend([
                {
                    "type": "投资建议",
                    "title": "适合长期持有",
                    "content": "该股票风险较低，适合长期投资者持有"
                },
                {
                    "type": "操作策略",
                    "title": "分批建仓",
                    "content": "建议分批次建仓，降低平均成本"
                }
            ])
        elif risk_score > 60:
            recommendations.extend([
                {
                    "type": "风险提示",
                    "title": "高风险警告",
                    "content": "该股票风险较高，请谨慎投资"
                },
                {
                    "type": "操作策略",
                    "title": "严格止损",
                    "content": "建议设置严格的止损位，控制风险"
                }
            ])
        else:
            recommendations.extend([
                {
                    "type": "投资建议",
                    "title": "适度配置",
                    "content": "建议适度配置，不宜重仓"
                }
            ])
        
        # 通用建议
        recommendations.extend([
            {
                "type": "监控要点",
                "title": "关注财报发布",
                "content": "密切关注公司财报和业绩指引"
            },
            {
                "type": "市场观察",
                "title": "跟踪行业动态",
                "content": "关注行业发展趋势和政策变化"
            }
        ])
        
        return recommendations

# 快捷函数
async def get_stock_advice(symbol: str) -> Dict[str, Any]:
    """获取股票投资建议"""
    advisor = StockAdvisor()
    return await advisor.get_professional_advice(symbol)

def get_stock_advice_sync(symbol: str) -> Dict[str, Any]:
    """同步获取股票投资建议"""
    import asyncio
    return asyncio.run(get_stock_advice(symbol))

if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test():
        advisor = StockAdvisor()
        advice = await advisor.get_professional_advice("600519")
        print(json.dumps(advice, ensure_ascii=False, indent=2))
    
    asyncio.run(test())