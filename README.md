# 🚀 MCP股票顾问服务

一个基于MCP（Model Context Protocol）的专业股票投资建议服务，提供实时股票数据获取和四维度投资分析。

## ✨ 功能特色

- 📊 **实时股票数据** - 基于东方财富API获取最新股票信息
- 🔍 **四维度分析** - 基本面、技术面、资金流向、市场情绪综合分析
- 💡 **专业投资建议** - 量化评分系统，提供具体的投资建议
- 🎯 **风险控制** - 精确的目标价位和止损价位建议
- 🔧 **易于集成** - 标准MCP协议，支持多种客户端

## 🎬 快速演示

```bash
# 获取600136恒瑞医药的投资建议
python get_600136_advice.py
```

输出示例：
```
📊 600136 专业投资建议分析报告
============================================================
📈 股票基本信息:
   股票代码: 600136
   股票名称: 恒瑞医药
   当前价格: 45.67元
   涨跌幅: +1.23%

🔍 四维度分析:
   基本面分析: 85.0/100 - 基本面优秀
   技术面分析: 70.0/100 - 技术面强势
   资金流向: 75.0/100 - 资金大幅流入
   市场情绪: 80.0/100 - 市场情绪乐观

💡 投资建议:
   综合评分: 74.0/100
   投资建议: 推荐 👍
   目标价位: 50.24元
   止损价位: 42.93元
```

## 🚀 快速开始

### 方式一：一键安装（推荐）

#### Windows用户
1. 下载项目到本地
2. 双击运行 `install.bat`
3. 双击桌面快捷方式启动服务

#### Linux/Mac用户
```bash
# 克隆项目
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service

# 一键安装
chmod +x install.sh
./install.sh

# 启动服务
./start_service.sh
```

### 方式二：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service

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

## 📋 系统要求

- Python 3.8+
- 网络连接（获取实时股票数据）
- 内存：至少512MB
- 磁盘空间：至少100MB

## 🔧 使用方法

### MCP客户端调用

```python
import asyncio
from mcp import Client
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(command=["python", "stock_advisor_server.py"]) as (read, write):
        async with Client(read, write) as client:
            await client.initialize()
            
            # 获取专业投资建议
            result = await client.call_tool(
                "get_professional_investment_advice",
                arguments={"symbol": "600136"}
            )
            print(result)

asyncio.run(main())
```

### 命令行工具

```bash
# 获取特定股票建议
python get_stock_advice.py 600136

# 批量分析
python batch_analysis.py 600136,000001,000002
```

## 📊 支持的功能

### 核心工具

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `get_stock_price` | 获取实时股票价格 | `symbol`: 股票代码 |
| `get_professional_investment_advice` | 获取专业投资建议 | `symbol`: 股票代码 |
| `search_stock_by_name` | 按名称搜索股票 | `name`: 股票名称 |
| `get_comprehensive_analysis` | 获取综合分析报告 | `symbol`: 股票代码 |

### 分析维度

1. **基本面分析** (权重30%)
   - PE估值评估
   - 市值稳定性
   - 财务健康度

2. **技术面分析** (权重30%)
   - 价格趋势分析
   - 成交量分析
   - 技术指标评估

3. **资金流向分析** (权重25%)
   - 主力资金流向
   - 大单分析
   - 资金活跃度

4. **市场情绪分析** (权重15%)
   - 新闻关注度
   - 成交量情绪
   - 市场热度

## 📈 投资建议等级

| 评分区间 | 投资建议 | 信心水平 | 目标涨幅 | 止损幅度 | 建议仓位 |
|---------|---------|---------|---------|---------|---------|
| 75-100  | 强烈推荐 | 高      | +15%    | -8%     | 重仓    |
| 65-74   | 推荐     | 较高    | +10%    | -6%     | 标准仓位 |
| 55-64   | 谨慎关注 | 中等    | +5%     | -4%     | 轻仓    |
| 45-54   | 观望     | 中等    | +2%     | -2%     | 空仓    |
| 0-44    | 回避     | 高      | -2%     | -5%     | 空仓    |

## 🛠️ 配置说明

### 环境变量

```bash
# 可选配置
export MCP_PORT=8080                    # MCP服务端口
export DATA_SOURCE=eastmoney            # 数据源选择
export CACHE_TIMEOUT=300                # 缓存超时时间（秒）
export LOG_LEVEL=INFO                   # 日志级别
```

### 配置文件

创建 `config.json`：
```json
{
    "data_sources": {
        "primary": "eastmoney",
        "fallback": "tonghuashun"
    },
    "cache": {
        "enabled": true,
        "timeout": 300
    },
    "analysis": {
        "weights": {
            "fundamental": 0.3,
            "technical": 0.3,
            "money_flow": 0.25,
            "sentiment": 0.15
        }
    }
}
```

## 📊 API响应示例

### 获取股票价格
```json
{
    "symbol": "600136",
    "name": "恒瑞医药",
    "current_price": 45.67,
    "change": 0.56,
    "change_percent": 1.24,
    "volume": 2345678,
    "market_cap": "2800亿",
    "pe_ratio": 35.2,
    "timestamp": "2024-01-15T10:30:00"
}
```

### 获取投资建议
```json
{
    "symbol": "600136",
    "name": "恒瑞医药",
    "current_price": 45.67,
    "overall_score": 74.0,
    "recommendation": "推荐",
    "confidence": "较高",
    "target_price": 50.24,
    "stop_loss": 42.93,
    "risk_level": "中",
    "analysis": {
        "fundamental_analysis": {"score": 85.0, "assessment": "优秀"},
        "technical_analysis": {"score": 70.0, "assessment": "较好"},
        "money_flow_analysis": {"score": 75.0, "assessment": "较好"},
        "market_sentiment": {"score": 80.0, "assessment": "良好"}
    }
}
```

## 🐛 故障排除

### 常见问题

1. **无法获取股票数据**
   - 检查网络连接
   - 确认股票代码是否正确
   - 查看日志获取详细错误信息

2. **MCP服务启动失败**
   - 检查端口是否被占用
   - 确认Python版本兼容性
   - 检查依赖包是否完整

3. **分析结果不准确**
   - 检查数据源是否正常
   - 确认缓存是否过期
   - 查看权重配置是否合理

### 调试模式

```bash
# 启用调试模式
python stock_advisor_server.py --debug

# 查看详细日志
python stock_advisor_server.py --debug 2>&1 | tee debug.log
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境搭建

```bash
# 1. 克隆项目
git clone https://github.com/F415643/stock-advisor-mcp-service.git

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 运行测试
python -m pytest tests/
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙋‍♂️ 联系我们

- 📧 Issues：[GitHub Issues](https://github.com/F415643/stock-advisor-mcp-service/issues)

## 🔄 更新日志

### v1.0.0 (2024-01-15)
- ✨ 初始版本发布
- 📊 实现四维度股票分析
- 🔍 集成东方财富API
- 📈 添加投资建议系统
- 🐳 支持Docker部署

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！