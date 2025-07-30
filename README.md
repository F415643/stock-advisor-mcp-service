# 🚀 MCP股票数据服务

一个基于MCP（Model Context Protocol）的股票数据获取和分析服务，提供实时股票数据查询、技术指标计算和数据分析功能。

## 📋 服务介绍

MCP股票数据服务是一个专业的股票数据分析工具，通过东方财富API获取实时数据，提供多维度的股票数据查询和技术分析功能。服务支持股票基本信息查询、技术指标计算和数据可视化展示。

### ✨ 核心功能

- 📊 **实时股票数据** - 基于东方财富API获取最新股票信息
- 🔍 **多维度分析** - 基本面、技术面、资金流向、市场情绪数据分析
- ⚡ **技术指标计算** - 基于均线、MFI、换手率等技术指标的数据计算
- 💡 **数据查询服务** - 提供股票基本信息和历史数据查询
- 📈 **数据可视化** - 支持股票数据的图表展示和分析
- 🔧 **易于集成** - 标准MCP协议，支持多种客户端

## 🚀 快速开始

### 方式一：一键安装（推荐）

#### Windows用户
1. 下载项目到本地
2. 双击运行 `install.bat`
3. 双击桌面快捷方式启动服务

#### Linux/Mac用户
```bash
# 克隆项目
git clone https://github.com/yourusername/mcp-stock-advisor.git
cd mcp-stock-advisor

# 一键安装
chmod +x install.sh
./install.sh

# 启动服务
./start_service.sh
```

### 方式二：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/mcp-stock-advisor.git
cd mcp-stock-advisor

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动MCP服务
python stock_advisor_server.py --name "股票建议助手" --debug
```

### 方式三：Docker部署

```bash
# 使用Docker Compose
docker-compose up -d

# 或者直接使用Docker
docker build -t mcp-stock-advisor .
docker run -p 8080:8080 mcp-stock-advisor
```

## 📊 服务功能

### 核心工具

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `get_stock_price` | 获取实时股票价格 | `symbol`: 股票代码 |
| `get_stock_data` | 获取股票基本数据 | `symbol`: 股票代码 |
| `get_technical_indicators` | 获取技术指标数据 | `symbol`: 股票代码 |
| `search_stock_by_name` | 按名称搜索股票 | `name`: 股票名称 |
| `get_market_data` | 获取市场数据分析 | `symbol`: 股票代码 |

### 数据分析维度

#### 基本面数据分析

1. **财务数据**
   - PE比率计算
   - 市值数据
   - 财务指标

2. **技术面数据**
   - 价格趋势数据
   - 成交量数据
   - 技术指标计算

3. **资金流向数据**
   - 资金流向统计
   - 大单数据分析
   - 资金活跃度指标

4. **市场数据**
   - 市场关注度
   - 成交量统计
   - 市场热度指标

#### 技术指标计算

1. **均线指标**
   - MA5 (5日均线)
   - MA20 (20日均线)
   - 均线关系分析

2. **动量指标**
   - MFI (资金流量指数)
   - 换手率计算
   - RSI (相对强弱指数)

3. **趋势指标**
   - 趋势方向判断
   - 支撑阻力位计算

## 🎬 使用示例

### 获取股票数据

```python
import asyncio
from mcp_client import MCPClient

async def main():
    client = MCPClient()
    
    # 获取股票基本数据
    data = await client.call_tool(
        "get_stock_data",
        {"symbol": "600136"}
    )
    print(data)

    # 获取技术指标数据
    indicators = await client.call_tool(
        "get_technical_indicators",
        {"symbol": "600136"}
    )
    print(indicators)

asyncio.run(main())
```

### 命令行工具

```bash
# 获取特定股票数据
python get_stock_data.py 600136

# 获取技术指标分析
python get_technical_analysis.py 600136

# 批量数据查询
python batch_query.py 600136,000001,000002
```

## 🛠️ 服务配置

### 服务配置 (Server Config)

```json
{
  "name": "stock-data-service",
  "display_name": "股票数据服务",
  "description": "提供股票数据查询和技术分析的MCP服务",
  "version": "1.0.0",
  "author": "Your Name",
  "license": "MIT",
  "homepage": "https://github.com/yourusername/mcp-stock-advisor",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/mcp-stock-advisor.git"
  },
  "main": "stock_advisor_server.py",
  "env": {
    "MCP_PORT": "8080",
    "DATA_SOURCE": "eastmoney",
    "CACHE_TIMEOUT": "300",
    "LOG_LEVEL": "INFO"
  },
  "tools": [
    {
      "name": "get_stock_price",
      "description": "获取实时股票价格",
      "parameters": {
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
    {
      "name": "get_stock_data",
      "description": "获取股票基本数据",
      "parameters": {
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
    {
      "name": "get_technical_indicators",
      "description": "获取技术指标数据",
      "parameters": {
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
  ],
  "resources": [
    {
      "name": "stock_info",
      "description": "股票基本信息",
      "uri": "/stock/{symbol}/info"
    }
  ]
}
```

### 环境变量

```bash
# 可选配置
export MCP_PORT=8080                    # MCP服务端口
export DATA_SOURCE=eastmoney            # 数据源选择
export CACHE_TIMEOUT=300                # 缓存超时时间（秒）
export LOG_LEVEL=INFO                   # 日志级别
```

## 📋 系统要求

- Python 3.8+
- 网络连接（获取实时股票数据）
- 内存：至少512MB
- 磁盘空间：至少100MB

## 🔍 故障排除

### 常见问题

**Q: 服务启动失败**
```bash
# 检查端口占用
netstat -an | grep 8080

# 检查Python版本
python --version

# 检查依赖安装
pip list | grep fastmcp
```

**Q: 数据获取失败**
```bash
# 测试网络连接
ping push2.eastmoney.com

# 检查防火墙设置
# 确保可以访问外部API
```

### 日志查看

```bash
# 查看服务日志
tail -f mcp-stock.log

# 调试模式启动
python stock_advisor_server.py --debug --log-level DEBUG
```

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。


⭐ 如果这个项目对你有帮助，请给我们一个星标！

**免责声明**: 本服务仅提供股票数据查询和技术分析功能，所有数据仅供参考，不构成任何投资建议。用户应当根据自身情况谨慎使用相关数据。
