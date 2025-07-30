#!/usr/bin/env python3
"""
专业投资建议演示脚本
展示如何使用MCP股票顾问服务获取专业投资建议
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from get_stock_advice import get_stock_advice_sync
from get_enhanced_investment_advice import get_enhanced_advice_sync

def print_header(title):
    """打印标题"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_section(title, content):
    """打印章节"""
    print(f"\n【{title}】")
    if isinstance(content, dict):
        print(json.dumps(content, ensure_ascii=False, indent=2))
    else:
        print(content)

def format_currency(amount):
    """格式化货币"""
    return f"¥{amount:,.2f}"

def format_percentage(value):
    """格式化百分比"""
    return f"{value:.2f}%"

def analyze_stock_basic(symbol, advice):
    """分析股票基本信息"""
    print_header(f"股票 {symbol} 基础分析报告")
    
    if "error" in advice:
        print(f"错误: {advice['error']}")
        return
    
    # 基础信息
    basic_info = {
        "股票代码": symbol,
        "分析时间": advice.get("advice_date", ""),
        "当前价格": format_currency(advice.get("current_price", 0))
    }
    print_section("基本信息", basic_info)
    
    # 投资建议
    investment_advice = advice.get("advice", {})
    print_section("投资建议", {
        "总体建议": investment_advice.get("recommendation", ""),
        "操作建议": investment_advice.get("action", ""),
        "信心水平": investment_advice.get("confidence", ""),
        "综合评分": f"{investment_advice.get('score', 0)}/100"
    })
    
    # 风险等级
    risk_level = advice.get("risk_level", {})
    print_section("风险评估", {
        "风险等级": risk_level.get("risk_level", ""),
        "风险颜色": risk_level.get("risk_color", ""),
        "风险评分": f"{risk_level.get('risk_score', 0):.1f}/100"
    })
    
    # 交易信号
    trading_signals = advice.get("trading_signals", {})
    print_section("交易信号", trading_signals)
    
    # 目标价位
    target_prices = advice.get("target_prices", {})
    print_section("目标价位", target_prices)

def analyze_stock_enhanced(symbol, advice):
    """分析增强版股票信息"""
    print_header(f"股票 {symbol} 增强版分析报告")
    
    if "error" in advice:
        print(f"错误: {advice['error']}")
        return
    
    # 增强分析
    enhanced_analysis = advice.get("enhanced_analysis", {})
    print_section("增强分析", {
        "动量分析": enhanced_analysis.get("momentum_analysis", {}),
        "波动率分析": enhanced_analysis.get("volatility_analysis", {})
    })
    
    # 个性化建议
    personalized_advice = advice.get("personalized_advice", {})
    print_section("个性化建议", personalized_advice)
    
    # 情景分析
    scenario_analysis = advice.get("scenario_analysis", {})
    print_section("情景分析", {
        "牛市情景": scenario_analysis.get("bull_scenario", {}),
        "熊市情景": scenario_analysis.get("bear_scenario", {}),
        "基准情景": scenario_analysis.get("base_scenario", {})
    })

def run_basic_analysis():
    """运行基础分析演示"""
    print_header("MCP股票顾问服务 - 基础分析演示")
    
    # 演示股票列表
    demo_stocks = ["600519", "000858", "601318", "000001"]
    
    print("正在分析以下股票的基础投资建议...")
    
    for symbol in demo_stocks:
        print(f"\n分析股票: {symbol}")
        print("-" * 40)
        
        try:
            advice = get_stock_advice_sync(symbol)
            analyze_stock_basic(symbol, advice)
        except Exception as e:
            print(f"分析 {symbol} 时出错: {e}")

def run_enhanced_analysis():
    """运行增强分析演示"""
    print_header("MCP股票顾问服务 - 增强分析演示")
    
    # 演示股票
    symbol = "600519"
    
    print(f"正在对 {symbol} 进行增强版投资建议分析...")
    
    try:
        # 不同投资期限和风险偏好的分析
        scenarios = [
            {"horizon": "short", "risk": "conservative", "name": "短期保守"},
            {"horizon": "medium", "risk": "moderate", "name": "中期中性"},
            {"horizon": "long", "risk": "aggressive", "name": "长期激进"}
        ]
        
        for scenario in scenarios:
            print(f"\n{scenario['name']}投资策略分析")
            print("=" * 50)
            
            advice = get_enhanced_advice_sync(
                symbol, 
                investment_horizon=scenario["horizon"],
                risk_tolerance=scenario["risk"]
            )
            analyze_stock_enhanced(symbol, advice)
            
    except Exception as e:
        print(f"增强分析时出错: {e}")

def run_performance_comparison():
    """运行性能对比演示"""
    print_header("性能对比分析")
    
    symbol = "000858"
    
    print(f"正在对比 {symbol} 的基础分析和增强分析性能...")
    
    # 记录开始时间
    start_time = datetime.now()
    
    # 基础分析
    basic_advice = get_stock_advice_sync(symbol)
    basic_time = datetime.now()
    
    # 增强分析
    enhanced_advice = get_enhanced_advice_sync(symbol)
    enhanced_time = datetime.now()
    
    # 计算耗时
    basic_duration = (basic_time - start_time).total_seconds()
    enhanced_duration = (enhanced_time - basic_time).total_seconds()
    
    # 结果对比
    comparison = {
        "基础分析耗时": f"{basic_duration:.2f}秒",
        "增强分析耗时": f"{enhanced_duration:.2f}秒",
        "性能提升": f"{((enhanced_duration - basic_duration) / basic_duration * 100):.1f}%",
        "功能对比": {
            "基础分析": ["投资建议", "风险评估", "交易信号", "目标价位"],
            "增强分析": [
                "基础分析全部功能",
                "动量分析", "波动率分析", "相关性分析",
                "个性化建议", "情景分析", "投资组合建议",
                "高级指标", "市场时机", "行业分析"
            ]
        }
    }
    
    print_section("性能对比结果", comparison)

def run_risk_assessment_demo():
    """运行风险评估演示"""
    print_header("风险评估演示")
    
    # 不同风险等级的股票
    risk_stocks = ["601318", "600519", "300750"]
    
    print("正在评估不同股票的风险等级...")
    
    risk_analysis = []
    for symbol in risk_stocks:
        try:
            advice = get_stock_advice_sync(symbol)
            if "error" not in advice:
                risk_info = {
                    "股票代码": symbol,
                    "风险等级": advice.get("risk_level", {}).get("risk_level", ""),
                    "风险评分": advice.get("risk_level", {}).get("risk_score", 0),
                    "投资建议": advice.get("advice", {}).get("recommendation", "")
                }
                risk_analysis.append(risk_info)
        except Exception as e:
            print(f"评估 {symbol} 风险时出错: {e}")
    
    print_section("风险等级评估结果", risk_analysis)

def run_portfolio_suggestion_demo():
    """运行投资组合建议演示"""
    print_header("投资组合建议演示")
    
    # 模拟投资组合
    portfolio_stocks = ["600519", "000858", "601318", "000001"]
    
    print("正在生成投资组合建议...")
    
    portfolio_analysis = []
    for symbol in portfolio_stocks:
        try:
            advice = get_enhanced_advice_sync(
                symbol, 
                investment_horizon="medium",
                risk_tolerance="moderate"
            )
            if "error" not in advice:
                portfolio_info = {
                    "股票代码": symbol,
                    "建议配置比例": advice.get("personalized_advice", {}).get("allocation_advice", {}).get("recommended_allocation", ""),
                    "风险调整": advice.get("personalized_advice", {}).get("allocation_advice", {}).get("position_sizing", {}),
                    "入场时机": advice.get("personalized_advice", {}).get("timing_advice", {}).get("entry_timing", "")
                }
                portfolio_analysis.append(portfolio_info)
        except Exception as e:
            print(f"分析 {symbol} 投资组合时出错: {e}")
    
    print_section("投资组合建议", portfolio_analysis)

def main():
    """主函数"""
    print("="*80)
    print("MCP股票顾问服务 - 专业投资建议演示")
    print("="*80)
    print("本演示展示如何使用MCP股票顾问服务获取专业投资建议")
    print("包括基础分析和增强版分析功能")
    
    # 演示选项
    demos = {
        "1": ("基础分析演示", run_basic_analysis),
        "2": ("增强分析演示", run_enhanced_analysis),
        "3": ("性能对比演示", run_performance_comparison),
        "4": ("风险评估演示", run_risk_assessment_demo),
        "5": ("投资组合建议演示", run_portfolio_suggestion_demo),
        "6": ("运行全部演示", lambda: [run_basic_analysis(), run_enhanced_analysis(), 
                                     run_performance_comparison(), run_risk_assessment_demo(),
                                     run_portfolio_suggestion_demo()])
    }
    
    print("\n请选择演示项目:")
    for key, (name, _) in demos.items():
        print(f"{key}. {name}")
    
    print("\n或者直接按回车运行全部演示...")
    
    try:
        choice = input("\n请选择 (1-6): ").strip()
        
        if choice in demos:
            demos[choice][1]()
        else:
            print("运行全部演示...")
            demos["6"][1]()
            
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"演示运行出错: {e}")
    
    print("\n" + "="*80)
    print("演示完成！感谢使用MCP股票顾问服务")
    print("="*80)

if __name__ == "__main__":
    main()