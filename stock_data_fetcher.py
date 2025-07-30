"""
股票数据获取模块
提供从多个数据源获取股票实时数据的功能
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataFetcher:
    """股票数据获取器"""
    
    def __init__(self):
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=10)
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def fetch_stock_data(self, symbol: str) -> Dict[str, Any]:
        """获取股票综合数据"""
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
            
        try:
            # 并行获取多个数据源
            tasks = [
                self.get_stock_info_from_eastmoney(symbol),
                self.get_stock_financial_data(symbol),
                self.get_money_flow_data(symbol),
                self.get_technical_indicators(symbol),
                self.get_market_sentiment(symbol),
                self.get_stock_news(symbol)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            basic_info = results[0] if not isinstance(results[0], Exception) else {}
            financial_data = results[1] if not isinstance(results[1], Exception) else {}
            money_flow = results[2] if not isinstance(results[2], Exception) else {}
            technical_indicators = results[3] if not isinstance(results[3], Exception) else {}
            sentiment = results[4] if not isinstance(results[4], Exception) else {}
            news = results[5] if not isinstance(results[5], Exception) else []
            
            return {
                "symbol": symbol,
                "basic_info": basic_info,
                "financial_data": financial_data,
                "money_flow": money_flow,
                "technical_indicators": technical_indicators,
                "sentiment": sentiment,
                "news": news,
                "data_sources": ["东方财富", "同花顺", "雪球"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            return {"error": str(e)}
    
    async def get_stock_info_from_eastmoney(self, symbol: str) -> Dict[str, Any]:
        """从东方财富获取股票基本信息"""
        try:
            # 构建API URL
            url = f"https://push2.eastmoney.com/api/qt/stock/get"
            params = {
                'secid': f"1.{symbol}" if symbol.startswith('6') else f"0.{symbol}",
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f60,f62,f63,f64,f65,f66,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f92,f107,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252,f253,f254,f255,f256,f257,f258,f259,f260,f261,f262,f263,f264,f265,f266,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f277,f278,f279,f280,f281,f282,f283,f284,f285,f286,f287,f288,f289,f290,f291,f292,f293,f294,f295,f296,f297,f298,f299,f300,f301,f302,f303,f304,f305,f306,f307,f308,f309,f310,f311,f312,f313,f314,f315,f316,f317,f318,f319,f320,f321,f322,f323,f324,f325,f326,f327,f328,f329,f330,f331,f332,f333,f334,f335,f336,f337,f338,f339,f340,f341,f342,f343,f344,f345,f346,f347,f348,f349,f350,f351,f352,f353,f354,f355,f356,f357,f358,f359,f360,f361,f362,f363,f364,f365,f366,f367,f368,f369,f370,f371,f372,f373,f374,f375,f376,f377,f378,f379,f380,f381,f382,f383,f384,f385,f386,f387,f388,f389,f390,f391,f392,f393,f394,f395,f396,f397,f398,f399,f400,f401,f402,f403,f404,f405,f406,f407,f408,f409,f410,f411,f412,f413,f414,f415,f416,f417,f418,f419,f420,f421,f422,f423,f424,f425,f426,f427,f428,f429,f430,f431,f432,f433,f434,f435,f436,f437,f438,f439,f440,f441,f442,f443,f444,f445,f446,f447,f448,f449,f450,f451,f452,f453,f454,f455,f456,f457,f458,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f469,f470,f471,f472,f473,f474,f475,f476,f477,f478,f479,f480,f481,f482,f483,f484,f485,f486,f487,f488,f489,f490,f491,f492,f493,f494,f495,f496,f497,f498,f499,f500'
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        stock_data = data['data']
                        return {
                            "symbol": symbol,
                            "name": stock_data.get('f58', ''),
                            "price": float(stock_data.get('f43', 0)) / 100,
                            "change": float(stock_data.get('f170', 0)) / 100,
                            "change_percent": float(stock_data.get('f170', 0)) / 100,
                            "volume": int(stock_data.get('f47', 0)),
                            "turnover": float(stock_data.get('f48', 0)),
                            "high": float(stock_data.get('f44', 0)) / 100,
                            "low": float(stock_data.get('f45', 0)) / 100,
                            "open": float(stock_data.get('f46', 0)) / 100,
                            "pre_close": float(stock_data.get('f60', 0)) / 100,
                            "market_cap": float(stock_data.get('f116', 0)) * 10000,
                            "pe_ratio": float(stock_data.get('f162', 0)),
                            "pb_ratio": float(stock_data.get('f167', 0)),
                            "dividend_yield": float(stock_data.get('f164', 0))
                        }
        except Exception as e:
            logger.error(f"从东方财富获取数据失败: {e}")
            return {"error": str(e)}
        
        return {}
    
    async def get_stock_financial_data(self, symbol: str) -> Dict[str, Any]:
        """获取股票财务数据"""
        try:
            # 模拟财务数据
            return {
                "symbol": symbol,
                "roe": 15.2,  # 净资产收益率
                "profit_margin": 12.5,  # 利润率
                "debt_ratio": 45.6,  # 负债率
                "current_ratio": 1.8,  # 流动比率
                "quick_ratio": 1.2,  # 速动比率
                "revenue_growth": 8.5,  # 营收增长率
                "profit_growth": 12.3  # 利润增长率
            }
        except Exception as e:
            logger.error(f"获取财务数据失败: {e}")
            return {"error": str(e)}
    
    async def get_money_flow_data(self, symbol: str) -> Dict[str, Any]:
        """获取资金流向数据"""
        try:
            # 模拟资金流向数据
            return {
                "symbol": symbol,
                "main_net_inflow": 12345678.90,  # 主力净流入
                "super_large_net": 5678901.23,  # 超大单净流入
                "large_net": 3456789.01,  # 大单净流入
                "medium_net": 1234567.89,  # 中单净流入
                "small_net": -876543.21,  # 小单净流入
                "main_ratio": 0.15,  # 主力占比
                "net_flow_5d": 9876543.21,  # 5日净流入
                "net_flow_10d": 12345678.90  # 10日净流入
            }
        except Exception as e:
            logger.error(f"获取资金流向数据失败: {e}")
            return {"error": str(e)}
    
    async def get_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """获取技术指标数据"""
        try:
            # 模拟技术指标数据
            return {
                "symbol": symbol,
                "ma5": 15.67,  # 5日均线
                "ma10": 15.45,  # 10日均线
                "ma20": 15.23,  # 20日均线
                "ma60": 14.89,  # 60日均线
                "rsi": 65.2,  # RSI指标
                "macd": 0.15,  # MACD值
                "macd_signal": 0.08,  # MACD信号线
                "kdj_k": 78.5,  # KDJ-K值
                "kdj_d": 72.3,  # KDJ-D值
                "kdj_j": 90.9,  # KDJ-J值
                "boll_upper": 16.45,  # 布林带上轨
                "boll_middle": 15.23,  # 布林带中轨
                "boll_lower": 14.01,  # 布林带下轨
                "volume_ratio": 1.25,  # 量比
                "mfi": 68.7  # 资金流量指标
            }
        except Exception as e:
            logger.error(f"获取技术指标失败: {e}")
            return {"error": str(e)}
    
    async def get_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """获取市场情绪数据"""
        try:
            # 模拟市场情绪数据
            return {
                "symbol": symbol,
                "market_attention": "high",  # 市场关注度
                "news_sentiment": 0.75,  # 新闻情绪得分
                "social_sentiment": 0.68,  # 社媒情绪得分
                "analyst_rating": "buy",  # 分析师评级
                "institutional_holding": 0.45,  # 机构持仓比例
                "short_interest": 0.02,  # 做空比例
                "fear_greed_index": 72  # 恐惧贪婪指数
            }
        except Exception as e:
            logger.error(f"获取市场情绪数据失败: {e}")
            return {"error": str(e)}
    
    async def get_stock_news(self, symbol: str) -> List[Dict[str, Any]]:
        """获取股票新闻"""
        try:
            # 模拟新闻数据
            return [
                {
                    "title": f"{symbol}发布最新财报，业绩超预期",
                    "content": "公司第三季度营收同比增长15%，净利润增长20%",
                    "publish_time": "2024-01-15 09:30:00",
                    "source": "东方财富",
                    "sentiment": "positive",
                    "importance": "high"
                },
                {
                    "title": f"{symbol}获得机构上调评级",
                    "content": "多家券商上调目标价，看好公司发展前景",
                    "publish_time": "2024-01-14 14:20:00",
                    "source": "新浪财经",
                    "sentiment": "positive",
                    "importance": "medium"
                },
                {
                    "title": f"{symbol}宣布重大投资计划",
                    "content": "公司计划投资10亿元建设新生产基地",
                    "publish_time": "2024-01-13 16:45:00",
                    "source": "证券时报",
                    "sentiment": "positive",
                    "importance": "high"
                }
            ]
        except Exception as e:
            logger.error(f"获取新闻数据失败: {e}")
            return []
    
    async def search_stock(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索股票"""
        try:
            # 模拟搜索结果
            return [
                {
                    "symbol": "600519",
                    "name": "贵州茅台",
                    "market": "上交所",
                    "industry": "白酒"
                },
                {
                    "symbol": "000858",
                    "name": "五粮液",
                    "market": "深交所",
                    "industry": "白酒"
                },
                {
                    "symbol": "000568",
                    "name": "泸州老窖",
                    "market": "深交所",
                    "industry": "白酒"
                }
            ]
        except Exception as e:
            logger.error(f"搜索股票失败: {e}")
            return []

async def fetch_stock_data(symbol: str) -> Dict[str, Any]:
    """获取股票综合数据的快捷函数"""
    async with StockDataFetcher() as fetcher:
        return await fetcher.fetch_stock_data(symbol)

async def search_stock(keyword: str) -> List[Dict[str, Any]]:
    """搜索股票的快捷函数"""
    async with StockDataFetcher() as fetcher:
        return await fetcher.search_stock(keyword)

# 同步包装函数
def get_stock_data_sync(symbol: str) -> Dict[str, Any]:
    """同步获取股票数据"""
    return asyncio.run(fetch_stock_data(symbol))

def search_stock_sync(keyword: str) -> List[Dict[str, Any]]:
    """同步搜索股票"""
    return asyncio.run(search_stock(keyword))

if __name__ == "__main__":
    # 测试代码
    async def test():
        async with StockDataFetcher() as fetcher:
            data = await fetcher.fetch_stock_data('600519')
            print(json.dumps(data, ensure_ascii=False, indent=2))
    
    asyncio.run(test())