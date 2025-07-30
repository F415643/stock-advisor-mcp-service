# 🚀 MCP股票顾问服务

一个基于FastMCP的专业股票投资建议系统，提供实时股票数据获取和多维度投资分析。

## ✨ 功能特色

- 📊 **实时股票数据** - 集成同花顺、东方财富等多数据源
- 🔍 **四维度分析** - 基本面、技术面、资金流向、市场情绪综合分析
- 💡 **智能投资建议** - 基于量化模型的专业投资建议
- 🎯 **风险控制** - 精确的目标价位和止损价位建议
- 🔧 **标准MCP协议** - 支持Claude Desktop、Cursor等主流客户端

## 🎬 快速开始

### 方式一：一键安装（推荐）

#### Windows用户
```bash
# 克隆项目
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service

# 一键安装
双击 install.bat

# 启动服务
双击 start_server.bat
```

#### Linux/Mac用户
```bash
# 克隆项目
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service

# 一键安装
chmod +x install.sh
./install.sh

# 启动服务
python start_server.py
```

### 方式二：Docker部署

```bash
# 使用Docker Compose
docker-compose up -d

# 或者直接使用Docker
docker build -t mcp-stock-advisor .
docker run -p 8080:8080 mcp-stock-advisor
```

### 方式三：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动MCP服务
python stock_advisor_server.py
```

## 📋 系统要求

- **Python**: 3.8+
- **网络**: 需要连接互联网获取实时股票数据
- **内存**: 至少512MB
- **磁盘**: 至少100MB可用空间

## 🔧 使用方法

### MCP客户端配置

#### Claude Desktop配置
在`claude_desktop_config.json`中添加：

```json
{
  "mcpServers": {
    "stock-advisor": {
      "command": "python",
      "args": ["path/to/stock_advisor_server.py"],
      "env": {
        "PYTHONPATH": "path/to/stock-advisor-mcp-service"
      }
    }
  }
}
```

#### Cursor配置
在`.cursor/mcp.json`中添加：

```json
{
  "mcpServers": {
    "stock-advisor": {
      "command": "python",
      "args": ["path/to/stock_advisor_server.py"]
    }
  }
}
```

### 核心工具调用

#### 1. 获取股票价格
```python
# MCP客户端调用
result = await mcp_client.call_tool(
    "get_stock_price",
    {"symbol": "600136"}
)
```

#### 2. 获取专业投资建议
```python
# MCP客户端调用
result = await mcp_client.call_tool(
    "get_professional_investment_advice",
    {"symbol": "600136"}
)
```

#### 3. 获取增强版投资建议
```python
# MCP客户端调用
result = await mcp_client.call_tool(
    "get_enhanced_investment_advice",
    {"symbol": "600136", "analysis_type": "long_term"}
)
```

#### 4. 搜索股票
```python
# MCP客户端调用
result = await mcp_client.call_tool(
    "search_stock_by_name",
    {"name": "恒瑞医药"}
)
```

### 命令行使用

#### 获取股票建议
```bash
# 获取单个股票建议
python get_stock_advice.py 600136

# 获取增强版投资建议
python get_enhanced_investment_advice.py 600136 --type long_term

# 运行演示脚本
python demo_professional_advice.py
```

#### 批量分析
```bash
# 批量分析多个股票
python batch_analysis.py 600136,000001,000002
```

## 📊 功能详解

### 核心工具

| 工具名称 | 功能描述 | 参数说明 | 返回数据 |
|---------|---------|----------|----------|
| `get_stock_price` | 获取实时股票价格 | `symbol`: 股票代码 | 当前价格、涨跌幅、成交量 |
| `get_professional_investment_advice` | 获取专业投资建议 | `symbol`: 股票代码 | 综合评分、建议、目标价、止损价 |
| `get_enhanced_investment_advice` | 获取增强版投资建议 | `symbol`: 股票代码, `analysis_type`: 分析类型 | 详细分析报告、技术指标、资金流向 |
| `search_stock_by_name` | 按名称搜索股票 | `name`: 股票名称 | 匹配的股票列表、代码、当前价 |
| `get_comprehensive_analysis` | 获取综合分析报告 | `symbol`: 股票代码 | 四维度详细分析、投资建议 |

### 分析维度

#### 1. 基本面分析 (权重30%)
- **估值评估**: PE、PB、PEG等估值指标
- **财务健康**: 营收增长、净利润增长、ROE
- **市场地位**: 市值规模、行业地位

#### 2. 技术面分析 (权重30%)
- **趋势分析**: 短期、中期、长期趋势
- **技术指标**: MACD、KDJ、RSI、BOLL
- **支撑阻力**: 关键价位分析

#### 3. 资金流向分析 (权重25%)
- **主力动向**: 大单资金流入流出
- **资金活跃度**: 成交量、换手率
- **机构持仓**: 机构持股变化

#### 4. 市场情绪分析 (权重15%)
- **新闻情绪**: 近期新闻情感分析
- **市场热度**: 搜索热度、关注度
- **舆情监控**: 社交媒体情绪

### 投资建议等级

| 综合评分 | 投资建议 | 信心水平 | 目标涨幅 | 止损幅度 | 建议仓位 |
|---------|---------|---------|---------|---------|---------|
| 80-100  | 强烈推荐 | 高      | +15-20% | -8%     | 重仓70% |
| 70-79   | 推荐     | 较高    | +10-15% | -6%     | 标准50% |
| 60-69   | 谨慎关注 | 中等    | +5-10%  | -4%     | 轻仓30% |
| 50-59   | 观望     | 中等    | +2-5%   | -2%     | 空仓0%  |
| 0-49    | 回避     | 高      | -2-5%   | -5%     | 空仓0%  |

## ⚙️ 配置说明

### 环境变量

```bash
# 服务配置
export MCP_HOST=localhost           # MCP服务主机
export MCP_PORT=8080               # MCP服务端口
export DEBUG=false                 # 调试模式

# 数据配置
export DATA_SOURCE=eastmoney       # 数据源选择
export CACHE_TIMEOUT=300           # 缓存超时时间（秒）
export MAX_RETRIES=3               # 最大重试次数

# 日志配置
export LOG_LEVEL=INFO              # 日志级别
export LOG_FILE=mcp-stock.log      # 日志文件
```

### 配置文件 (config.json)

```json
{
  "server": {
    "host": "localhost",
    "port": 8080,
    "debug": false,
    "name": "股票建议助手"
  },
  "data": {
    "source": "eastmoney",
    "cache_timeout": 300,
    "max_retries": 3,
    "timeout": 10
  },
  "analysis": {
    "fundamental_weight": 0.30,
    "technical_weight": 0.30,
    "money_flow_weight": 0.25,
    "sentiment_weight": 0.15,
    "min_score_threshold": 50
  },
  "logging": {
    "level": "INFO",
    "file": "mcp-stock.log",
    "max_size": "10MB",
    "backup_count": 5
  }
}
```

## 📚 示例代码

### 基础使用示例

```python
#!/usr/bin/env python3
import asyncio
import json
from stock_data_fetcher import fetch_stock_data

async def analyze_stock(symbol):
    """分析单个股票"""
    try:
        data = await fetch_stock_data(symbol)
        
        if data and data.get('basic_info'):
            basic = data['basic_info']
            print(f"📊 {symbol} 股票信息")
            print(f"股票名称: {basic.get('name')}")
            print(f"当前价格: {basic.get('price'):.2f}元")
            print(f"涨跌幅: {basic.get('change_percent'):+.2f}%")
            print(f"成交量: {basic.get('volume'):,}手")
            
            return data
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    asyncio.run(analyze_stock('600136'))
```

### 高级分析示例

```python
#!/usr/bin/env python3
import asyncio
import json
from get_enhanced_investment_advice import get_enhanced_advice

async def detailed_analysis(symbols):
    """详细股票分析"""
    results = {}
    
    for symbol in symbols:
        try:
            # 获取增强版投资建议
            advice = await get_enhanced_advice(symbol, analysis_type="long_term")
            results[symbol] = advice
            
            print(f"✅ {symbol} 分析完成")
            
        except Exception as e:
            print(f"❌ {symbol} 分析失败: {e}")
    
    # 保存结果
    with open('enhanced_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

# 批量分析
if __name__ == "__main__":
    symbols = ['600136', '000001', '000002', '600519', '600036']
    asyncio.run(detailed_analysis(symbols))
```

## 🔍 故障排除

### 常见问题及解决方案

#### 1. 服务启动失败

```bash
# 检查端口占用
netstat -ano | findstr 8080    # Windows
lsof -i :8080                  # Linux/Mac

# 检查Python版本
python --version
# 要求 Python 3.8+

# 检查依赖安装
pip list | grep -E "(fastmcp|aiohttp|requests)"
```

#### 2. 数据获取失败

```bash
# 测试网络连接
ping push2.eastmoney.com

# 检查API访问权限
# 确保可以访问东方财富等数据源

# 检查日志
python stock_advisor_server.py --debug
```

#### 3. 内存使用过高

```bash
# 调整缓存设置
export CACHE_TIMEOUT=60

# 限制并发
export MAX_CONCURRENT_REQUESTS=5

# 使用轻量级模式
export LIGHTWEIGHT_MODE=true
```

#### 4. MCP客户端连接失败

```bash
# 检查服务状态
curl http://localhost:8080/health

# 检查配置文件
# 确保MCP客户端配置正确

# 查看详细日志
python stock_advisor_server.py --log-level DEBUG
```

### 日志查看与调试

```bash
# 查看实时日志
tail -f mcp-stock.log

# 调试模式启动
python stock_advisor_server.py --debug --log-level DEBUG

# 测试单个功能
python -c "
import asyncio
from stock_data_fetcher import fetch_stock_price
async def test():
    result = await fetch_stock_price('600136')
    print(result)
asyncio.run(test())
"
```

### 性能优化

```bash
# 启用缓存
export CACHE_TIMEOUT=300

# 调整并发设置
export MAX_WORKERS=10

# 使用CDN加速
export USE_CDN=true
```

## 🤝 贡献指南

我们热烈欢迎社区贡献！以下是参与方式：

### 快速开始贡献

1. **Fork 项目**
   - 点击右上角的Fork按钮

2. **克隆到本地**
   ```bash
   git clone https://github.com/your-username/stock-advisor-mcp-service.git
   cd stock-advisor-mcp-service
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

4. **开发环境设置**
   ```bash
   # 安装开发依赖
   pip install -r requirements-dev.txt
   
   # 运行测试
   python -m pytest tests/
   
   # 代码格式化
   black .
   isort .
   flake8 .
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add AmazingFeature"
   git push origin feature/AmazingFeature
   ```

6. **开启 Pull Request**
   - 在GitHub上创建PR
   - 描述清楚功能变更
   - 添加测试用例

### 代码规范

- **提交信息**: 遵循Conventional Commits
- **代码风格**: 使用Black格式化，PEP8标准
- **测试覆盖**: 新功能必须包含测试
- **文档更新**: 更新相关文档

### 开发路线图

- [ ] 支持更多数据源（雪球、新浪财经等）
- [ ] 增加技术指标分析
- [ ] 实现实时推送功能
- [ ] 添加Web界面
- [ ] 支持美股港股
- [ ] 机器学习预测模型

## 📄 许可证

本项目采用 **MIT 许可证** - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

### 数据源支持
- [东方财富](https://www.eastmoney.com/) - 主要股票数据API
- [同花顺](https://www.10jqka.com.cn/) - 补充数据源
- [新浪财经](https://finance.sina.com.cn/) - 实时行情数据

### 开源项目
- [FastMCP](https://gofastmcp.com/) - MCP服务框架
- [Python](https://python.org/) - 开发语言
- [aiohttp](https://docs.aiohttp.org/) - 异步HTTP客户端

## 📞 联系我们

### 问题反馈
- 🐛 **Bug报告**: [GitHub Issues](https://github.com/F415643/stock-advisor-mcp-service/issues)
- 💡 **功能建议**: [GitHub Discussions](https://github.com/F415643/stock-advisor-mcp-service/discussions)
- 📧 **邮件联系**: F415643@users.noreply.github.com

### 社区支持
- 📱 **微信群**: 扫描下方二维码加入技术交流群
- 💬 **Discord**: [加入Discord社区](https://discord.gg/stock-advisor)
- 🐦 **Twitter**: [@StockAdvisorMCP](https://twitter.com/StockAdvisorMCP)

## 🔗 相关链接

### 官方文档
- [MCP协议文档](https://modelcontextprotocol.io/)
- [FastMCP文档](https://gofastmcp.com/docs)
- [项目Wiki](https://github.com/F415643/stock-advisor-mcp-service/wiki)

### API参考
- [东方财富API文档](https://www.eastmoney.com/api)
- [股票代码对照表](https://github.com/F415643/stock-advisor-mcp-service/blob/main/docs/stock_codes.md)

### 教程资源
- [MCP开发指南](https://github.com/F415643/stock-advisor-mcp-service/blob/main/docs/mcp_guide.md)
- [部署教程](https://github.com/F415643/stock-advisor-mcp-service/blob/main/docs/deployment.md)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=F415643/stock-advisor-mcp-service&type=Date)](https://star-history.com/#F415643/stock-advisor-mcp-service&Date)

**如果这个项目对你有帮助，请给我们一个⭐星标支持！**

---

## ⚠️ 免责声明

**重要提示：投资风险声明**

> 本服务提供的所有投资建议仅供参考，不构成具体的投资建议。股市有风险，投资需谨慎。请根据自身的风险承受能力和投资经验做出独立的投资决策。使用本服务即表示您已充分理解并接受投资风险，本服务不对任何投资损失承担责任。

**数据准确性声明**

> 本服务使用的股票数据来源于第三方公开API，虽然我们会尽力确保数据的准确性，但无法保证数据的完整性和实时性。建议用户在做出投资决策前，通过其他渠道核实相关数据。

---

**最后更新**: 2024年12月
**版本**: v1.0.0
**维护者**: [@F415643](https://github.com/F415643)