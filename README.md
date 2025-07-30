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

### 1. 基础服务配置 (Server Config)

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
    },
    {
      "name": "search_stock_by_name",
      "description": "按名称搜索股票",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "股票名称"
          }
        },
        "required": ["name"]
      }
    },
    {
      "name": "get_market_data",
      "description": "获取市场数据分析",
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
    },
    {
      "name": "technical_data",
      "description": "技术指标数据",
      "uri": "/stock/{symbol}/technical"
    }
  ]
}
```

### 2. MCP客户端配置

#### 标准MCP配置 (`mcp-config.json`)
```json
{
  "mcpServers": {
    "stock-data-service": {
      "command": "python",
      "args": ["MCP/stock_advisor_server.py", "--name", "股票数据服务"],
      "env": {
        "MCP_PORT": "8080",
        "DATA_SOURCE": "eastmoney",
        "CACHE_TIMEOUT": "300",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### Claude Desktop配置
```json
{
  "mcpServers": {
    "stock-data-service": {
      "command": "python",
      "args": ["d:/trae代码/魔塔MCP/MCP/stock_advisor_server.py", "--name", "股票数据服务"],
      "env": {
        "PYTHONPATH": "d:/trae代码/魔塔MCP"
      }
    }
  }
}
```

**配置文件位置**：
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### 3. 环境变量配置

#### 基础环境变量
```bash
# 服务端口配置
export MCP_PORT=8080                    # MCP服务端口

# 数据源配置
export DATA_SOURCE=eastmoney            # 数据源选择 (eastmoney/tencent/sina)

# 缓存配置
export CACHE_TIMEOUT=300                # 缓存超时时间（秒）
export ENABLE_CACHE=true                # 是否启用缓存

# 日志配置
export LOG_LEVEL=INFO                   # 日志级别 (DEBUG/INFO/WARNING/ERROR)
export LOG_FILE=mcp-stock.log           # 日志文件路径

# 性能配置
export MAX_CONCURRENT_REQUESTS=10       # 最大并发请求数
export REQUEST_TIMEOUT=30               # 请求超时时间（秒）
```

#### 高级环境变量
```bash
# API配置
export EASTMONEY_API_KEY=""             # 东方财富API密钥（可选）
export RATE_LIMIT_PER_MINUTE=100        # 每分钟请求限制

# 安全配置
export ENABLE_AUTH=false                # 是否启用认证
export API_KEYS="key1,key2,key3"        # API密钥列表

# 数据库配置（可选）
export DB_HOST=localhost                # 数据库主机
export DB_PORT=5432                     # 数据库端口
export DB_NAME=stock_data               # 数据库名称
export DB_USER=postgres                 # 数据库用户
export DB_PASSWORD=""                   # 数据库密码
```

### 4. Docker配置

#### Dockerfile配置
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY MCP/ ./MCP/
COPY *.py ./

# 设置环境变量
ENV MCP_PORT=8080
ENV DATA_SOURCE=eastmoney
ENV LOG_LEVEL=INFO

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# 启动命令
CMD ["python", "MCP/stock_advisor_server.py", "--name", "股票数据服务"]
```

#### Docker Compose配置
```yaml
version: '3.8'
services:
  stock-data-service:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - MCP_PORT=8080
      - DATA_SOURCE=eastmoney
      - CACHE_TIMEOUT=300
      - LOG_LEVEL=INFO
      - ENABLE_CACHE=true
      - MAX_CONCURRENT_REQUESTS=10
    volumes:
      - ./logs:/app/logs
      - ./cache:/app/cache
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8080/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - stock-network

  # Redis缓存服务（可选）
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - stock-network

volumes:
  redis_data:

networks:
  stock-network:
    driver: bridge
```

### 5. 配置文件管理

#### 创建配置文件 (`config.json`)
```json
{
  "server": {
    "name": "股票数据服务",
    "port": 8080,
    "debug": false,
    "max_workers": 4
  },
  "data": {
    "source": "eastmoney",
    "cache_timeout": 300,
    "retry_times": 3,
    "request_timeout": 30
  },
  "logging": {
    "level": "INFO",
    "file": "logs/mcp-stock.log",
    "max_size": "10MB",
    "backup_count": 5
  },
  "security": {
    "enable_auth": false,
    "api_keys": [],
    "rate_limit": {
      "requests_per_minute": 100,
      "burst_size": 10
    }
  },
  "features": {
    "enable_cache": true,
    "enable_metrics": true,
    "enable_health_check": true
  }
}
```

#### 加载配置的Python代码
```python
import json
import os
from typing import Dict, Any

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        "server": {"name": "股票数据服务", "port": 8080, "debug": False},
        "data": {"source": "eastmoney", "cache_timeout": 300},
        "logging": {"level": "INFO", "file": "mcp-stock.log"}
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # 合并默认配置
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in config[key]:
                        config[key][sub_key] = sub_value
        return config
    else:
        return default_config

# 使用示例
config = load_config()
server_port = config["server"]["port"]
data_source = config["data"]["source"]
```

### 6. 命令行参数配置

```bash
# 基础启动
python stock_advisor_server.py

# 指定服务名称
python stock_advisor_server.py --name "股票数据服务"

# 启用调试模式
python stock_advisor_server.py --debug

# 指定端口
python stock_advisor_server.py --port 8080

# 指定配置文件
python stock_advisor_server.py --config config.json

# 指定日志级别
python stock_advisor_server.py --log-level DEBUG

# 组合使用
python stock_advisor_server.py --name "股票数据服务" --debug --port 8080 --log-level INFO
```

### 7. 配置验证

#### 配置检查脚本
```python
#!/usr/bin/env python3
"""配置验证脚本"""

import json
import os
import sys

def validate_config():
    """验证配置文件"""
    errors = []
    
    # 检查必需的环境变量
    required_env = ["MCP_PORT", "DATA_SOURCE"]
    for env_var in required_env:
        if not os.getenv(env_var):
            errors.append(f"缺少环境变量: {env_var}")
    
    # 检查端口是否可用
    port = int(os.getenv("MCP_PORT", 8080))
    if not (1024 <= port <= 65535):
        errors.append(f"端口号无效: {port}")
    
    # 检查数据源配置
    data_source = os.getenv("DATA_SOURCE", "eastmoney")
    if data_source not in ["eastmoney", "tencent", "sina"]:
        errors.append(f"不支持的数据源: {data_source}")
    
    # 检查日志级别
    log_level = os.getenv("LOG_LEVEL", "INFO")
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        errors.append(f"无效的日志级别: {log_level}")
    
    if errors:
        print("配置验证失败:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("配置验证通过!")

if __name__ == "__main__":
    validate_config()
```

### 8. 配置最佳实践

#### 开发环境配置
```bash
# .env.development
MCP_PORT=8080
DATA_SOURCE=eastmoney
LOG_LEVEL=DEBUG
ENABLE_CACHE=false
MAX_CONCURRENT_REQUESTS=5
```

#### 生产环境配置
```bash
# .env.production
MCP_PORT=8080
DATA_SOURCE=eastmoney
LOG_LEVEL=INFO
ENABLE_CACHE=true
MAX_CONCURRENT_REQUESTS=20
ENABLE_AUTH=true
```

#### 测试环境配置
```bash
# .env.test
MCP_PORT=8081
DATA_SOURCE=mock
LOG_LEVEL=DEBUG
ENABLE_CACHE=false
REQUEST_TIMEOUT=10
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
