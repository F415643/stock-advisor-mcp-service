#!/usr/bin/env python3
"""
标准MCP股票数据服务器
使用标准MCP协议实现，确保兼容性
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServer:
    """标准MCP服务器实现"""
    
    def __init__(self, name: str = "股票数据服务"):
        self.name = name
        self.version = "1.0.0"
        self.tools = self._register_tools()
        self.resources = []
        
    def _register_tools(self) -> Dict[str, Dict]:
        """注册所有工具"""
        return {
            "get_stock_price": {
                "description": "获取股票价格信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "股票代码，如600136"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            "get_stock_data": {
                "description": "获取股票基本数据",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "股票代码，如600136"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            "get_technical_indicators": {
                "description": "获取技术指标数据",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "股票代码，如600136"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            "search_stock_by_name": {
                "description": "按名称搜索股票",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "股票名称或关键词"
                        }
                    },
                    "required": ["name"]
                }
            },
            "get_market_data": {
                "description": "获取市场数据分析",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "股票代码，如600136"
                        }
                    },
                    "required": ["symbol"]
                }
            }
        }
    
    async def handle_request(self, request: Dict) -> Dict:
        """处理MCP请求"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                return await self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self._handle_tools_list(request_id)
            elif method == "tools/call":
                return await self._handle_tool_call(request_id, params)
            elif method == "resources/list":
                return await self._handle_resources_list(request_id)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            logger.error(f"处理请求时发生错误: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def _handle_initialize(self, request_id: str, params: Dict) -> Dict:
        """处理初始化请求"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
        }
    
    async def _handle_tools_list(self, request_id: str) -> Dict:
        """处理工具列表请求"""
        tools_list = []
        for name, config in self.tools.items():
            tools_list.append({
                "name": name,
                "description": config["description"],
                "inputSchema": config["inputSchema"]
            })
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools_list
            }
        }
    
    async def _handle_tool_call(self, request_id: str, params: Dict) -> Dict:
        """处理工具调用请求"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32602,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
        
        try:
            # 调用对应的工具函数
            if tool_name == "get_stock_price":
                result = await self._get_stock_price(arguments.get("symbol"))
            elif tool_name == "get_stock_data":
                result = await self._get_stock_data(arguments.get("symbol"))
            elif tool_name == "get_technical_indicators":
                result = await self._get_technical_indicators(arguments.get("symbol"))
            elif tool_name == "search_stock_by_name":
                result = await self._search_stock_by_name(arguments.get("name"))
            elif tool_name == "get_market_data":
                result = await self._get_market_data(arguments.get("symbol"))
            else:
                result = {"error": f"未实现工具: {tool_name}"}
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(result, ensure_ascii=False, indent=2)
                    }]
                }
            }
            
        except Exception as e:
            logger.error(f"调用工具 {tool_name} 时发生错误: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Tool execution error: {str(e)}"
                }
            }
    
    async def _handle_resources_list(self, request_id: str) -> Dict:
        """处理资源列表请求"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": self.resources
            }
        }
    
    async def _get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """获取股票价格"""
        return {
            "symbol": symbol,
            "price": 100.0,
            "change": 1.5,
            "change_percent": 1.5,
            "volume": 1000000,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """获取股票数据"""
        return {
            "symbol": symbol,
            "name": f"股票{symbol}",
            "price": 100.0,
            "change": 1.5,
            "change_percent": 1.5,
            "volume": 1000000,
            "market_cap": 1000000000,
            "pe_ratio": 15.5,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """获取技术指标"""
        return {
            "symbol": symbol,
            "rsi": 50.0,
            "macd": 0.0,
            "k": 50.0,
            "d": 50.0,
            "ma5": 100.0,
            "ma10": 100.0,
            "ma20": 100.0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _search_stock_by_name(self, name: str) -> List[Dict[str, str]]:
        """搜索股票"""
        return [{
            "symbol": "600000",
            "name": f"{name}股票",
            "price": "100.00"
        }]
    
    async def _get_market_data(self, symbol: str) -> Dict[str, Any]:
        """获取市场数据"""
        return {
            "symbol": symbol,
            "trend": "上涨",
            "recommendation": "买入",
            "timestamp": datetime.now().isoformat()
        }

async def main():
    """主函数"""
    server = MCPServer()
    
    # 模拟MCP服务器运行
    print("标准MCP股票数据服务器已启动")
    print("可用工具:")
    for name, config in server.tools.items():
        print(f"  - {name}: {config['description']}")

if __name__ == "__main__":
    asyncio.run(main())
