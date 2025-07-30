"""
技术分析模块
提供股票技术指标计算和分析功能
"""

import asyncio
import math
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """技术分析器"""
    
    def __init__(self):
        self.indicators = {}
    
    def calculate_ma(self, prices: List[float], period: int) -> float:
        """计算移动平均线"""
        if len(prices) < period:
            return 0.0
        return sum(prices[-period:]) / period
    
    def calculate_ema(self, prices: List[float], period: int) -> float:
        """计算指数移动平均线"""
        if len(prices) < period:
            return 0.0
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """计算RSI指标"""
        if len(prices) < period + 1:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return min(100, max(0, rsi))
    
    def calculate_macd(self, prices: List[float], 
                      fast_period: int = 12, 
                      slow_period: int = 26, 
                      signal_period: int = 9) -> Dict[str, float]:
        """计算MACD指标"""
        if len(prices) < slow_period:
            return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
        
        # 计算EMA
        fast_ema = self.calculate_ema(prices, fast_period)
        slow_ema = self.calculate_ema(prices, slow_period)
        
        macd_line = fast_ema - slow_ema
        
        # 计算信号线（MACD的EMA）
        macd_values = []
        for i in range(signal_period, len(prices) + 1):
            if i >= slow_period:
                fast = self.calculate_ema(prices[:i], fast_period)
                slow = self.calculate_ema(prices[:i], slow_period)
                macd_values.append(fast - slow)
        
        if len(macd_values) >= signal_period:
            signal_line = sum(macd_values[-signal_period:]) / signal_period
        else:
            signal_line = 0.0
        
        histogram = macd_line - signal_line
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram
        }
    
    def calculate_kdj(self, prices: List[float], 
                     highs: List[float], 
                     lows: List[float], 
                     period: int = 9) -> Dict[str, float]:
        """计算KDJ指标"""
        if len(prices) < period:
            return {"k": 50.0, "d": 50.0, "j": 50.0}
        
        # 计算RSV
        rsv_values = []
        for i in range(period - 1, len(prices)):
            period_high = max(highs[i-period+1:i+1])
            period_low = min(lows[i-period+1:i+1])
            
            if period_high == period_low:
                rsv = 50.0
            else:
                rsv = ((prices[i] - period_low) / (period_high - period_low)) * 100
            
            rsv_values.append(rsv)
        
        if not rsv_values:
            return {"k": 50.0, "d": 50.0, "j": 50.0}
        
        # 计算K、D、J值
        k_values = [50.0]
        d_values = [50.0]
        
        for rsv in rsv_values:
            k = (2/3) * k_values[-1] + (1/3) * rsv
            d = (2/3) * d_values[-1] + (1/3) * k
            
            k_values.append(k)
            d_values.append(d)
        
        k = k_values[-1]
        d = d_values[-1]
        j = 3 * k - 2 * d
        
        return {
            "k": min(100, max(0, k)),
            "d": min(100, max(0, d)),
            "j": min(100, max(0, j))
        }
    
    def calculate_bollinger_bands(self, prices: List[float], 
                                 period: int = 20, 
                                 std_dev: float = 2.0) -> Dict[str, float]:
        """计算布林带"""
        if len(prices) < period:
            return {"upper": 0.0, "middle": 0.0, "lower": 0.0}
        
        middle_band = self.calculate_ma(prices, period)
        
        # 计算标准差
        variance = sum((price - middle_band) ** 2 for price in prices[-period:]) / period
        std = math.sqrt(variance)
        
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return {
            "upper": upper_band,
            "middle": middle_band,
            "lower": lower_band
        }
    
    def calculate_volume_ratio(self, volumes: List[float], period: int = 5) -> float:
        """计算量比"""
        if len(volumes) < period + 1:
            return 1.0
        
        current_volume = volumes[-1]
        avg_volume = sum(volumes[-period-1:-1]) / period
        
        if avg_volume == 0:
            return 1.0
        
        return current_volume / avg_volume
    
    def calculate_mfi(self, prices: List[float], volumes: List[float], period: int = 14) -> float:
        """计算资金流量指标（MFI）"""
        if len(prices) < period + 1 or len(volumes) < period + 1:
            return 50.0
        
        typical_prices = [(prices[i] + max(prices[i], prices[i-1]) + min(prices[i], prices[i-1])) / 3 
                         for i in range(1, len(prices))]
        
        positive_flow = []
        negative_flow = []
        
        for i in range(1, len(typical_prices)):
            if typical_prices[i] > typical_prices[i-1]:
                positive_flow.append(typical_prices[i] * volumes[i])
                negative_flow.append(0)
            else:
                positive_flow.append(0)
                negative_flow.append(typical_prices[i] * volumes[i])
        
        if len(positive_flow) < period:
            return 50.0
        
        positive_money_flow = sum(positive_flow[-period:])
        negative_money_flow = sum(negative_flow[-period:])
        
        if negative_money_flow == 0:
            return 100.0
        
        money_ratio = positive_money_flow / negative_money_flow
        mfi = 100 - (100 / (1 + money_ratio))
        
        return min(100, max(0, mfi))
    
    def analyze_trend(self, prices: List[float]) -> Dict[str, Any]:
        """分析价格趋势"""
        if len(prices) < 5:
            return {"trend": "unknown", "strength": 0.0}
        
        # 计算短期和长期趋势
        short_ma = self.calculate_ma(prices, 5)
        long_ma = self.calculate_ma(prices, 20)
        
        current_price = prices[-1]
        
        # 判断趋势方向
        if current_price > short_ma > long_ma:
            trend = "bullish"
        elif current_price < short_ma < long_ma:
            trend = "bearish"
        else:
            trend = "sideways"
        
        # 计算趋势强度
        price_change = (prices[-1] - prices[0]) / prices[0] * 100
        volatility = self.calculate_volatility(prices)
        
        strength = min(100, abs(price_change) / (volatility + 0.001) * 10)
        
        return {
            "trend": trend,
            "strength": strength,
            "price_change": price_change,
            "volatility": volatility
        }
    
    def calculate_volatility(self, prices: List[float]) -> float:
        """计算价格波动率"""
        if len(prices) < 2:
            return 0.0
        
        returns = [(prices[i] - prices[i-1]) / prices[i-1] * 100 
                  for i in range(1, len(prices))]
        
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        
        return math.sqrt(variance)
    
    def generate_technical_report(self, symbol: str, 
                                 prices: List[float], 
                                 volumes: List[float]) -> Dict[str, Any]:
        """生成技术分析报告"""
        if len(prices) < 20:
            return {"error": "数据不足，需要至少20个数据点"}
        
        report = {
            "symbol": symbol,
            "analysis_date": datetime.now().isoformat(),
            "price_analysis": {
                "current_price": prices[-1],
                "price_change": (prices[-1] - prices[0]) / prices[0] * 100,
                "volatility": self.calculate_volatility(prices)
            },
            "moving_averages": {
                "ma5": self.calculate_ma(prices, 5),
                "ma10": self.calculate_ma(prices, 10),
                "ma20": self.calculate_ma(prices, 20),
                "ma60": self.calculate_ma(prices, 60)
            },
            "momentum_indicators": {
                "rsi": self.calculate_rsi(prices),
                "macd": self.calculate_macd(prices),
                "kdj": self.calculate_kdj(prices, prices, prices)
            },
            "volume_indicators": {
                "volume_ratio": self.calculate_volume_ratio(volumes),
                "mfi": self.calculate_mfi(prices, volumes)
            },
            "volatility_indicators": {
                "bollinger_bands": self.calculate_bollinger_bands(prices)
            },
            "trend_analysis": self.analyze_trend(prices)
        }
        
        # 生成交易信号
        signals = self.generate_trading_signals(report)
        report["trading_signals"] = signals
        
        return report
    
    def generate_trading_signals(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """生成交易信号"""
        signals = {
            "rsi_signal": "",
            "macd_signal": "",
            "kdj_signal": "",
            "ma_signal": "",
            "volume_signal": "",
            "overall_signal": ""
        }
        
        # RSI信号
        rsi = report["momentum_indicators"]["rsi"]
        if rsi > 70:
            signals["rsi_signal"] = "sell"
        elif rsi < 30:
            signals["rsi_signal"] = "buy"
        else:
            signals["rsi_signal"] = "hold"
        
        # MACD信号
        macd = report["momentum_indicators"]["macd"]
        if isinstance(macd, dict):
            macd_value = macd.get("macd", 0)
            signal_value = macd.get("signal", 0)
            
            if macd_value > signal_value and macd_value > 0:
                signals["macd_signal"] = "buy"
            elif macd_value < signal_value and macd_value < 0:
                signals["macd_signal"] = "sell"
            else:
                signals["macd_signal"] = "hold"
        
        # KDJ信号
        kdj = report["momentum_indicators"]["kdj"]
        k = kdj.get("k", 50)
        d = kdj.get("d", 50)
        
        if k > 80 and d > 80 and k < d:
            signals["kdj_signal"] = "sell"
        elif k < 20 and d < 20 and k > d:
            signals["kdj_signal"] = "buy"
        else:
            signals["kdj_signal"] = "hold"
        
        # 移动平均线信号
        ma5 = report["moving_averages"]["ma5"]
        ma20 = report["moving_averages"]["ma20"]
        current_price = report["price_analysis"]["current_price"]
        
        if current_price > ma5 > ma20:
            signals["ma_signal"] = "buy"
        elif current_price < ma5 < ma20:
            signals["ma_signal"] = "sell"
        else:
            signals["ma_signal"] = "hold"
        
        # 综合信号
        buy_signals = list(signals.values()).count("buy")
        sell_signals = list(signals.values()).count("sell")
        
        if buy_signals >= 3:
            signals["overall_signal"] = "strong_buy"
        elif buy_signals >= 2:
            signals["overall_signal"] = "buy"
        elif sell_signals >= 3:
            signals["overall_signal"] = "strong_sell"
        elif sell_signals >= 2:
            signals["overall_signal"] = "sell"
        else:
            signals["overall_signal"] = "hold"
        
        return signals

# 快捷函数
def analyze_stock_technical(symbol: str, 
                          prices: List[float], 
                          volumes: List[float]) -> Dict[str, Any]:
    """分析股票技术指标"""
    analyzer = TechnicalAnalyzer()
    return analyzer.generate_technical_report(symbol, prices, volumes)

if __name__ == "__main__":
    # 测试代码
    analyzer = TechnicalAnalyzer()
    
    # 模拟数据
    prices = [15.0, 15.2, 15.5, 15.3, 15.8, 15.6, 15.9, 16.2, 16.0, 16.3,
              16.1, 16.4, 16.2, 16.5, 16.3, 16.6, 16.4, 16.7, 16.5, 16.8,
              16.6, 16.9, 16.7, 17.0, 16.8, 17.1, 16.9, 17.2, 17.0, 17.3]
    
    volumes = [1000000, 1200000, 1100000, 1300000, 1250000, 1350000, 1400000, 1450000,
               1380000, 1420000, 1390000, 1440000, 1410000, 1460000, 1430000, 1480000,
               1450000, 1500000, 1470000, 1520000, 1490000, 1540000, 1510000, 1560000,
               1530000, 1580000, 1550000, 1600000, 1570000, 1620000]
    
    report = analyzer.generate_technical_report("600519", prices, volumes)
    import json
    print(json.dumps(report, ensure_ascii=False, indent=2))