#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小测试服务器，用于验证FastMCP工具注册
"""

from fastmcp import FastMCP, Context

# 创建MCP服务器实例
mcp = FastMCP(name="最小测试服务器")

@mcp.tool
async def get_investment_recommendation(symbol: str, investment_amount: float, risk_tolerance: str, ctx: Context) -> dict:
    """
    基于用户的投资金额和风险承受能力提供投资建议
    
    Args:
        symbol: 股票代码
        investment_amount: 投资金额（美元）
        risk_tolerance: 风险承受能力（"低", "中", "高"）
    
    Returns:
        个性化的投资建议
    """
    await ctx.info(f"正在为 {symbol} 生成投资建议...")
    
    # 简单的实现
    recommendation = {
        "symbol": symbol,
        "investment_amount": investment_amount,
        "risk_tolerance": risk_tolerance,
        "recommendation": "建议买入",
        "reasoning": ["这是一个测试建议"],
        "target_price": 100.0,
        "stop_loss": 90.0
    }
    
    await ctx.info(f"已生成 {symbol} 的投资建议")
    return recommendation

if __name__ == "__main__":
    print("启动最小测试服务器")
    print("可用工具: get_investment_recommendation")
    mcp.run()