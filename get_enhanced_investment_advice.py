"""
增强版投资建议生成模块
提供更深入的股票分析和投资建议
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import math

from stock_data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from get_stock_advice import StockAdvisor

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedStockAdvisor:
    """增强版股票投资建议生成器"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.tech_analyzer = TechnicalAnalyzer()
        self.base_advisor = StockAdvisor()
        
    async def get_enhanced_advice(self, symbol: str, 
                                 investment_horizon: str = "medium", 
                                 risk_tolerance: str = "moderate") -> Dict[str, Any]:
        """获取增强版投资建议"""
        try:
            # 获取基础数据
            stock_data = await self.data_fetcher.fetch_stock_data(symbol)
            
            if "error" in stock_data:
                return {"error": stock_data["error"]}
            
            # 获取基础建议
            base_advice = await self.base_advisor.get_professional_advice(symbol)
            
            # 增强分析
            enhanced_analysis = await self.perform_enhanced_analysis(stock_data)
            
            # 个性化建议
            personalized_advice = self.generate_personalized_advice(
                stock_data, investment_horizon, risk_tolerance
            )
            
            # 情景分析
            scenario_analysis = self.perform_scenario_analysis(stock_data)
            
            # 投资组合建议
            portfolio_advice = self.generate_portfolio_advice(
                stock_data, investment_horizon, risk_tolerance
            )
            
            return {
                "symbol": symbol,
                "analysis_date": datetime.now().isoformat(),
                "investment_horizon": investment_horizon,
                "risk_tolerance": risk_tolerance,
                "base_analysis": base_advice,
                "enhanced_analysis": enhanced_analysis,
                "personalized_advice": personalized_advice,
                "scenario_analysis": scenario_analysis,
                "portfolio_advice": portfolio_advice,
                "advanced_metrics": self.calculate_advanced_metrics(stock_data),
                "market_timing": self.analyze_market_timing(stock_data),
                "sector_analysis": await self.analyze_sector_performance(symbol),
                "competitive_analysis": await self.analyze_competitive_position(symbol),
                "valuation_models": self.perform_valuation_analysis(stock_data)
            }
            
        except Exception as e:
            logger.error(f"生成增强版投资建议失败: {e}")
            return {"error": str(e)}
    
    async def perform_enhanced_analysis(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行增强分析"""
        return {
            "momentum_analysis": self.analyze_momentum_patterns(stock_data),
            "volatility_analysis": self.analyze_volatility_patterns(stock_data),
            "correlation_analysis": await self.analyze_market_correlations(stock_data),
            "seasonal_analysis": self.analyze_seasonal_patterns(stock_data),
            "event_analysis": await self.analyze_market_events(stock_data),
            "behavioral_analysis": self.analyze_investor_behavior(stock_data)
        }
    
    def analyze_momentum_patterns(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析动量模式"""
        technical = stock_data.get("technical_indicators", {})
        
        # 多时间框架动量
        momentum_scores = {
            "short_term": self.calculate_momentum_score(technical, "short"),
            "medium_term": self.calculate_momentum_score(technical, "medium"),
            "long_term": self.calculate_momentum_score(technical, "long")
        }
        
        # 动量持续性
        momentum_sustainability = self.assess_momentum_sustainability(technical)
        
        # 动量转折点
        momentum_turning_points = self.identify_momentum_turning_points(technical)
        
        return {
            "momentum_scores": momentum_scores,
            "sustainability": momentum_sustainability,
            "turning_points": momentum_turning_points,
            "momentum_strength": self.calculate_overall_momentum_strength(momentum_scores)
        }
    
    def calculate_momentum_score(self, technical: Dict[str, Any], timeframe: str) -> float:
        """计算动量评分"""
        base_score = 50
        
        if timeframe == "short":
            # 短期动量（RSI, KDJ）
            rsi = technical.get("rsi", 50)
            kdj_k = technical.get("kdj_k", 50)
            
            rsi_contribution = (rsi - 50) * 0.8
            kdj_contribution = (kdj_k - 50) * 0.6
            
            base_score += rsi_contribution + kdj_contribution
            
        elif timeframe == "medium":
            # 中期动量（MACD, MA交叉）
            macd = technical.get("macd", {})
            ma5 = technical.get("ma5", 0)
            ma20 = technical.get("ma20", 0)
            
            macd_score = 0
            if isinstance(macd, dict):
                macd_value = macd.get("macd", 0)
                macd_score = max(-20, min(20, macd_value * 10))
            
            ma_score = 0
            if ma5 > ma20:
                ma_score = 15
            elif ma5 < ma20:
                ma_score = -15
            
            base_score += macd_score + ma_score
            
        elif timeframe == "long":
            # 长期动量（MA60, 趋势）
            ma20 = technical.get("ma20", 0)
            ma60 = technical.get("ma60", 0)
            
            if ma20 > ma60:
                base_score += 20
            else:
                base_score -= 20
        
        return max(0, min(100, base_score))
    
    def assess_momentum_sustainability(self, technical: Dict[str, Any]) -> Dict[str, Any]:
        """评估动量可持续性"""
        rsi = technical.get("rsi", 50)
        volume_ratio = technical.get("volume_ratio", 1)
        
        # 过度延伸风险
        overextended_risk = abs(rsi - 50) > 25
        
        # 成交量支持
        volume_support = volume_ratio > 1.2
        
        # 动量强度
        momentum_strength = min(100, max(0, 100 - abs(rsi - 50) * 2))
        
        return {
            "overextended_risk": overextended_risk,
            "volume_support": volume_support,
            "momentum_strength": momentum_strength,
            "sustainability_score": self.calculate_sustainability_score(
                overextended_risk, volume_support, momentum_strength
            )
        }
    
    def calculate_sustainability_score(self, overextended: bool, 
                                    volume_support: bool, 
                                    momentum_strength: float) -> float:
        """计算可持续性评分"""
        score = 50
        
        if not overextended:
            score += 20
        else:
            score -= 30
        
        if volume_support:
            score += 15
        else:
            score -= 15
        
        score += (momentum_strength - 50) * 0.3
        
        return max(0, min(100, score))
    
    def identify_momentum_turning_points(self, technical: Dict[str, Any]) -> Dict[str, Any]:
        """识别动量转折点"""
        rsi = technical.get("rsi", 50)
        macd = technical.get("macd", {})
        
        # 超买超卖信号
        oversold_signal = rsi < 30
        overbought_signal = rsi > 70
        
        # MACD背离检测
        macd_divergence = self.detect_macd_divergence(macd)
        
        return {
            "oversold_signal": oversold_signal,
            "overbought_signal": overbought_signal,
            "macd_divergence": macd_divergence,
            "turning_point_probability": self.calculate_turning_probability(
                oversold_signal, overbought_signal, macd_divergence
            )
        }
    
    def detect_macd_divergence(self, macd: Dict[str, Any]) -> str:
        """检测MACD背离"""
        if not isinstance(macd, dict):
            return "无数据"
        
        macd_value = macd.get("macd", 0)
        histogram = macd.get("histogram", 0)
        
        # 简化的背离检测逻辑
        if abs(histogram) < 0.05:
            return "潜在背离"
        elif macd_value > 0 and histogram < 0:
            return "顶背离"
        elif macd_value < 0 and histogram > 0:
            return "底背离"
        else:
            return "无背离"
    
    def calculate_turning_probability(self, oversold: bool, 
                                   overbought: bool, 
                                   divergence: str) -> float:
        """计算转折点概率"""
        probability = 10  # 基础概率
        
        if oversold or overbought:
            probability += 30
        
        if divergence in ["顶背离", "底背离"]:
            probability += 25
        elif divergence == "潜在背离":
            probability += 15
        
        return min(95, max(5, probability))
    
    def calculate_overall_momentum_strength(self, momentum_scores: Dict[str, float]) -> float:
        """计算整体动量强度"""
        weights = {"short_term": 0.4, "medium_term": 0.35, "long_term": 0.25}
        
        total_strength = sum(
            momentum_scores.get(period, 0) * weight 
            for period, weight in weights.items()
        )
        
        return max(0, min(100, total_strength))
    
    def generate_personalized_advice(self, stock_data: Dict[str, Any], 
                                   investment_horizon: str, 
                                   risk_tolerance: str) -> Dict[str, Any]:
        """生成个性化建议"""
        risk_assessment = self.assess_personalized_risk(
            stock_data, investment_horizon, risk_tolerance
        )
        
        allocation_advice = self.recommend_allocation(
            stock_data, investment_horizon, risk_tolerance
        )
        
        timing_advice = self.recommend_entry_timing(
            stock_data, investment_horizon
        )
        
        return {
            "risk_assessment": risk_assessment,
            "allocation_advice": allocation_advice,
            "timing_advice": timing_advice,
            "personalized_strategies": self.generate_strategies(
                stock_data, investment_horizon, risk_tolerance
            )
        }
    
    def assess_personalized_risk(self, stock_data: Dict[str, Any], 
                               investment_horizon: str, 
                               risk_tolerance: str) -> Dict[str, Any]:
        """评估个性化风险"""
        base_risk = self.calculate_risk_level(stock_data)
        
        # 根据投资期限调整风险
        horizon_multiplier = {
            "short": 1.5,  # 短期风险更高
            "medium": 1.0,
            "long": 0.8     # 长期风险较低
        }
        
        # 根据风险承受能力调整
        tolerance_multiplier = {
            "conservative": 1.2,
            "moderate": 1.0,
            "aggressive": 0.8
        }
        
        adjusted_risk = (
            base_risk.get("risk_score", 50) * 
            horizon_multiplier.get(investment_horizon, 1.0) * 
            tolerance_multiplier.get(risk_tolerance, 1.0)
        )
        
        return {
            "adjusted_risk_score": adjusted_risk,
            "suitability": self.determine_suitability(adjusted_risk, risk_tolerance),
            "risk_warnings": self.generate_risk_warnings(stock_data, adjusted_risk)
        }
    
    def determine_suitability(self, risk_score: float, risk_tolerance: str) -> str:
        """确定适合度"""
        tolerance_map = {
            "conservative": (0, 40),
            "moderate": (20, 70),
            "aggressive": (40, 100)
        }
        
        min_risk, max_risk = tolerance_map.get(risk_tolerance, (20, 70))
        
        if min_risk <= risk_score <= max_risk:
            return "适合"
        elif risk_score < min_risk:
            return "过于保守"
        else:
            return "风险过高"
    
    def generate_risk_warnings(self, stock_data: Dict[str, Any], risk_score: float) -> List[str]:
        """生成风险提示"""
        warnings = []
        
        if risk_score > 70:
            warnings.append("该股票风险较高，可能不适合保守投资者")
        
        pe_ratio = stock_data.get("basic_info", {}).get("pe_ratio", 0)
        if pe_ratio > 50:
            warnings.append("估值偏高，存在估值回调风险")
        
        volatility = abs(stock_data.get("technical_indicators", {}).get("rsi", 50) - 50)
        if volatility > 30:
            warnings.append("股价波动较大，短期可能出现较大回撤")
        
        return warnings
    
    def recommend_allocation(self, stock_data: Dict[str, Any], 
                           investment_horizon: str, 
                           risk_tolerance: str) -> Dict[str, Any]:
        """推荐配置比例"""
        base_score = 50  # 基础配置比例
        
        # 根据风险承受能力调整
        risk_multipliers = {
            "conservative": 0.5,
            "moderate": 1.0,
            "aggressive": 1.5
        }
        
        # 根据投资期限调整
        horizon_multipliers = {
            "short": 0.8,
            "medium": 1.0,
            "long": 1.2
        }
        
        adjusted_allocation = (
            base_score * 
            risk_multipliers.get(risk_tolerance, 1.0) * 
            horizon_multipliers.get(investment_horizon, 1.0)
        )
        
        # 限制在合理范围内
        max_allocation = min(30, max(5, adjusted_allocation))
        
        return {
            "recommended_allocation": f"{max_allocation:.1f}%",
            "rationale": f"基于{investment_horizon}期投资和{risk_tolerance}风险偏好",
            "position_sizing": self.calculate_position_sizing(stock_data, max_allocation)
        }
    
    def calculate_position_sizing(self, stock_data: Dict[str, Any], allocation: float) -> Dict[str, Any]:
        """计算仓位大小"""
        volatility = abs(stock_data.get("technical_indicators", {}).get("rsi", 50) - 50)
        
        # 基于波动率的仓位调整
        volatility_factor = 1 - (volatility / 100)
        
        adjusted_size = allocation * volatility_factor
        
        return {
            "base_position": f"{allocation:.1f}%",
            "volatility_adjusted": f"{adjusted_size:.1f}%",
            "max_position": f"{min(50, allocation * 2):.1f}%",
            "min_position": f"{max(2, allocation * 0.5):.1f}%"
        }
    
    def recommend_entry_timing(self, stock_data: Dict[str, Any], 
                             investment_horizon: str) -> Dict[str, Any]:
        """推荐入场时机"""
        technical = stock_data.get("technical_indicators", {})
        
        # 技术信号
        rsi = technical.get("rsi", 50)
        macd = technical.get("macd", {})
        
        # 入场时机评估
        entry_score = self.calculate_entry_timing_score(technical, investment_horizon)
        
        return {
            "entry_timing": self.determine_entry_timing(entry_score),
            "optimal_entry_range": self.calculate_entry_range(stock_data),
            "entry_strategies": self.generate_entry_strategies(entry_score, investment_horizon),
            "market_conditions": self.assess_market_conditions(stock_data)
        }
    
    def calculate_entry_timing_score(self, technical: Dict[str, Any], 
                                   investment_horizon: str) -> float:
        """计算入场时机评分"""
        score = 50
        
        rsi = technical.get("rsi", 50)
        volume_ratio = technical.get("volume_ratio", 1)
        
        # RSI时机
        if 30 <= rsi <= 70:
            score += 20
        elif rsi < 30:
            score += 30  # 超卖买入时机
        elif rsi > 70:
            score -= 20  # 超买谨慎
        
        # 成交量时机
        if volume_ratio > 1.5:
            score += 15  # 放量确认
        elif volume_ratio < 0.8:
            score -= 10  # 缩量谨慎
        
        return max(0, min(100, score))
    
    def determine_entry_timing(self, score: float) -> str:
        """确定入场时机"""
        if score >= 80:
            return "极佳买入时机"
        elif score >= 65:
            return "较好买入时机"
        elif score >= 50:
            return "中性时机"
        elif score >= 35:
            return "谨慎观望"
        else:
            return "建议等待"
    
    def calculate_entry_range(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算入场价格区间"""
        current_price = stock_data.get("basic_info", {}).get("price", 0)
        technical = stock_data.get("technical_indicators", {})
        
        support = technical.get("ma20", current_price) * 0.95
        resistance = technical.get("ma20", current_price) * 1.05
        
        return {
            "ideal_entry_range": f"{support:.2f} - {current_price:.2f}",
            "aggressive_entry": f"{current_price:.2f} - {resistance:.2f}",
            "conservative_entry": f"{support * 0.98:.2f} - {support:.2f}"
        }
    
    def generate_entry_strategies(self, score: float, 
                                investment_horizon: str) -> List[Dict[str, Any]]:
        """生成入场策略"""
        strategies = []
        
        if score >= 70:
            strategies.extend([
                {
                    "strategy": "一次性建仓",
                    "description": "在确认时机后一次性建立目标仓位",
                    "suitability": "激进投资者"
                },
                {
                    "strategy": "分批快速建仓",
                    "description": "在3-5个交易日内完成建仓",
                    "suitability": "中性投资者"
                }
            ])
        elif score >= 50:
            strategies.extend([
                {
                    "strategy": "分批建仓",
                    "description": "在2-4周内分批建立仓位",
                    "suitability": "稳健投资者"
                },
                {
                    "strategy": "定投策略",
                    "description": "定期定额投资，平滑成本",
                    "suitability": "长期投资者"
                }
            ])
        else:
            strategies.extend([
                {
                    "strategy": "等待确认",
                    "description": "等待更明确的技术信号再入场",
                    "suitability": "保守投资者"
                }
            ])
        
        return strategies
    
    def assess_market_conditions(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估市场条件"""
        technical = stock_data.get("technical_indicators", {})
        sentiment = stock_data.get("sentiment", {})
        
        # 市场状态判断
        market_state = "震荡"  # 默认状态
        
        rsi = technical.get("rsi", 50)
        if rsi < 30:
            market_state = "超卖"
        elif rsi > 70:
            market_state = "超买"
        elif 40 <= rsi <= 60:
            market_state = "平衡"
        
        return {
            "current_state": market_state,
            "market_regime": self.determine_market_regime(technical),
            "volatility_environment": self.assess_volatility_environment(technical),
            "liquidity_condition": self.assess_liquidity_condition(stock_data)
        }
    
    def determine_market_regime(self, technical: Dict[str, Any]) -> str:
        """确定市场状态"""
        ma5 = technical.get("ma5", 0)
        ma20 = technical.get("ma20", 0)
        ma60 = technical.get("ma60", 0)
        
        if ma5 > ma20 > ma60:
            return "上升趋势"
        elif ma5 < ma20 < ma60:
            return "下降趋势"
        else:
            return "震荡趋势"
    
    def assess_volatility_environment(self, technical: Dict[str, Any]) -> str:
        """评估波动率环境"""
        rsi = technical.get("rsi", 50)
        volatility = abs(rsi - 50)
        
        if volatility < 15:
            return "低波动"
        elif volatility < 30:
            return "中等波动"
        else:
            return "高波动"
    
    def assess_liquidity_condition(self, stock_data: Dict[str, Any]) -> str:
        """评估流动性状况"""
        volume = stock_data.get("basic_info", {}).get("volume", 0)
        
        if volume > 1000000:  # 100万股以上
            return "流动性良好"
        elif volume > 500000:
            return "流动性一般"
        else:
            return "流动性较差"
    
    def perform_scenario_analysis(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行情景分析"""
        current_price = stock_data.get("basic_info", {}).get("price", 0)
        
        # 牛市情景
        bull_scenario = {
            "probability": 25,
            "price_target": current_price * 1.3,
            "catalysts": ["业绩超预期", "政策利好", "行业景气度提升"],
            "timeframe": "3-6个月"
        }
        
        # 熊市情景
        bear_scenario = {
            "probability": 20,
            "price_target": current_price * 0.7,
            "catalysts": ["业绩不及预期", "政策收紧", "行业竞争加剧"],
            "timeframe": "3-6个月"
        }
        
        # 基准情景
        base_scenario = {
            "probability": 55,
            "price_target": current_price * 1.1,
            "catalysts": ["稳健增长", "行业平均表现"],
            "timeframe": "6-12个月"
        }
        
        return {
            "bull_scenario": bull_scenario,
            "bear_scenario": bear_scenario,
            "base_scenario": base_scenario,
            "expected_value": self.calculate_expected_value(
                [bull_scenario, bear_scenario, base_scenario]
            )
        }
    
    def calculate_expected_value(self, scenarios: List[Dict[str, Any]]) -> float:
        """计算期望值"""
        expected_value = 0
        
        for scenario in scenarios:
            probability = scenario.get("probability", 0) / 100
            price_target = scenario.get("price_target", 0)
            expected_value += probability * price_target
        
        return expected_value
    
    def generate_portfolio_advice(self, stock_data: Dict[str, Any], 
                                investment_horizon: str, 
                                risk_tolerance: str) -> Dict[str, Any]:
        """生成投资组合建议"""
        return {
            "diversification_strategy": self.recommend_diversification(
                stock_data, investment_horizon
            ),
            "hedging_strategy": self.recommend_hedging(stock_data, risk_tolerance),
            "rebalancing_frequency": self.recommend_rebalancing_frequency(investment_horizon),
            "monitoring_indicators": self.identify_key_indicators(stock_data)
        }
    
    def recommend_diversification(self, stock_data: Dict[str, Any], 
                              investment_horizon: str) -> Dict[str, Any]:
        """推荐分散化策略"""
        sector = "科技"  # 模拟行业
        
        return {
            "sector_allocation": f"{sector}行业不超过30%",
            "stock_correlation": "选择相关性低于0.7的股票",
            "geographic_diversification": "考虑港股和美股标的",
            "asset_allocation": "股票占60-80%，债券占20-40%"
        }
    
    def recommend_hedging(self, stock_data: Dict[str, Any], 
                       risk_tolerance: str) -> Dict[str, Any]:
        """推荐对冲策略"""
        return {
            "hedging_instruments": ["股指期货", "个股期权"],
            "hedging_ratio": "20-30%仓位对冲",
            "cost_analysis": "对冲成本约占收益的2-5%",
            "effectiveness": "可降低30-50%的下行风险"
        }
    
    def recommend_rebalancing_frequency(self, investment_horizon: str) -> str:
        """推荐再平衡频率"""
        frequency_map = {
            "short": "每周",
            "medium": "每月",
            "long": "每季度"
        }
        
        return frequency_map.get(investment_horizon, "每月")
    
    def identify_key_indicators(self, stock_data: Dict[str, Any]) -> List[str]:
        """识别关键指标"""
        return [
            "股价相对强弱指标(RSI)",
            "成交量变化",
            "MACD金叉/死叉",
            "20日均线支撑/阻力",
            "资金流向",
            "行业相对表现",
            "重要财报发布日期"
        ]

# 快捷函数
async def get_enhanced_investment_advice(symbol: str, 
                                       investment_horizon: str = "medium", 
                                       risk_tolerance: str = "moderate") -> Dict[str, Any]:
    """获取增强版投资建议"""
    advisor = EnhancedStockAdvisor()
    return await advisor.get_enhanced_advice(symbol, investment_horizon, risk_tolerance)

def get_enhanced_advice_sync(symbol: str, 
                           investment_horizon: str = "medium", 
                           risk_tolerance: str = "moderate") -> Dict[str, Any]:
    """同步获取增强版投资建议"""
    import asyncio
    return asyncio.run(get_enhanced_investment_advice(symbol, investment_horizon, risk_tolerance))

if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test():
        advisor = EnhancedStockAdvisor()
        advice = await advisor.get_enhanced_advice("600519", "medium", "moderate")
        print(json.dumps(advice, ensure_ascii=False, indent=2))
    
    asyncio.run(test())