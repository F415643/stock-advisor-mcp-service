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
from mcp_client import MCPClient

async def main():
    client = MCPClient()
    
    # 获取专业投资建议
    advice = await client.call_tool(
        "get_professional_investment_advice",
        {"symbol": "600136"}
    )
    print(advice)

asyncio.run(main())
```

### HTTP API调用

```bash
# 获取股票价格
curl http://localhost:8080/api/stock/price/600136

# 获取投资建议
curl http://localhost:8080/api/stock/advice/600136

# 搜索股票
curl http://localhost:8080/api/stock/search/恒瑞医药
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
  "server": {
    "name": "股票建议助手",
    "port": 8080,
    "debug": false
  },
  "data": {
    "source": "eastmoney",
    "cache_timeout": 300,
    "retry_times": 3
  },
  "analysis": {
    "fundamental_weight": 0.30,
    "technical_weight": 0.30,
    "money_flow_weight": 0.25,
    "sentiment_weight": 0.15
  }
}
```

## 📚 示例代码

### 基础使用示例

```python
#!/usr/bin/env python3
import asyncio
from stock_data_fetcher import fetch_stock_data

async def get_stock_analysis(symbol):
    """获取股票分析"""
    data = await fetch_stock_data(symbol)
    
    if data and data.get('basic_info'):
        basic = data['basic_info']
        print(f"股票名称: {basic.get('name')}")
        print(f"当前价格: {basic.get('price'):.2f}元")
        print(f"涨跌幅: {basic.get('change_percent'):+.2f}%")
    
    return data

# 使用示例
asyncio.run(get_stock_analysis('600136'))
```

### 批量分析示例

```python
import asyncio
import json

async def batch_analysis(symbols):
    """批量股票分析"""
    results = {}
    
    for symbol in symbols:
        try:
            data = await fetch_stock_data(symbol)
            results[symbol] = data
            print(f"✅ {symbol} 分析完成")
        except Exception as e:
            print(f"❌ {symbol} 分析失败: {e}")
    
    # 保存结果
    with open('batch_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

# 批量分析示例
symbols = ['600136', '000001', '000002', '600519']
asyncio.run(batch_analysis(symbols))
```

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

**Q: 内存使用过高**
```bash
# 调整缓存设置
export CACHE_TIMEOUT=60

# 限制并发请求
export MAX_CONCURRENT=5
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

### 开发环境设置

```bash
# 克隆开发版本
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/

# 代码格式化
black .
flake8 .
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [东方财富](https://www.eastmoney.com/) - 提供股票数据API
- [FastMCP](https://gofastmcp.com/) - MCP服务框架
- [Python](https://python.org/) - 开发语言

## 📞 联系我们

- 📧 邮箱: your-email@example.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/F415643/stock-advisor-mcp-service/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/F415643/stock-advisor-mcp-service/discussions)

## 🔗 相关链接

- [MCP协议文档](https://modelcontextprotocol.io/)
- [东方财富API文档](https://www.eastmoney.com/api)
- [项目Wiki](https://github.com/F415643/stock-advisor-mcp-service/wiki)

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！

**免责声明**: 本服务提供的投资建议仅供参考，不构成投资建议。投资有风险，入市需谨慎。请根据自身情况做出投资决策。