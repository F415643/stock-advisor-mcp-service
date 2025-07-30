# MCP股票顾问服务部署和使用指南

## 项目简介

MCP股票顾问服务是一个基于FastMCP框架的专业股票投资建议系统，支持多维度股票分析和智能投资建议生成。该系统集成了多个数据源，提供实时股票数据获取、技术分析、投资建议生成等功能。

## 功能特色

### 核心功能
- **四维度股票分析**: 基本面、技术面、消息面、资金面综合分析
- **多数据源支持**: 同花顺、东方财富、雪球等主流数据源
- **智能投资建议**: 基于AI算法的个性化投资建议
- **实时数据获取**: 实时股票价格、财务数据、资金流向
- **技术指标分析**: RSI、MACD、均线系统等主流技术指标
- **风险评估**: 综合风险评估和风险管理建议

### 增强功能
- **个性化建议**: 根据投资偏好和风险承受能力提供个性化建议
- **情景分析**: 牛市、熊市、基准情景下的投资回报预测
- **投资组合建议**: 基于风险分散的投资组合配置建议
- **市场时机**: 基于技术分析的市场时机判断
- **行业分析**: 行业对比和相对强弱分析

## 快速开始

### 环境要求
- Python 3.8+
- Docker (可选)
- Git

### 安装方式

#### 方式一：直接克隆使用
```bash
git clone https://github.com/F415643/stock-advisor-mcp-service.git
cd stock-advisor-mcp-service
pip install -r requirements.txt
```

#### 方式二：使用安装脚本
**Windows系统:**
```bash
install.bat
```

**Linux/Mac系统:**
```bash
chmod +x install.sh
./install.sh
```

#### 方式三：Docker部署
```bash
docker build -t mcp-stock-advisor .
docker run -p 8000:8000 mcp-stock-advisor
```

#### 方式四：Docker Compose
```bash
docker-compose up -d
```

## 使用方法

### 1. 启动服务

#### 开发模式启动
```bash
python start_server.py dev --host 0.0.0.0 --port 8000 --debug
```

#### 生产模式启动
```bash
python start_server.py start --host 0.0.0.0 --port 8000
```

#### Docker模式启动
```bash
python start_server.py docker
```

### 2. 基本使用

#### 获取股票建议
```python
from get_stock_advice import get_stock_advice_sync

# 获取基础投资建议
advice = get_stock_advice_sync("600519")
print(f"投资建议: {advice['advice']['recommendation']}")
print(f"风险等级: {advice['risk_level']['risk_level']}")
```

#### 获取增强版建议
```python
from get_enhanced_investment_advice import get_enhanced_advice_sync

# 获取增强版投资建议
enhanced_advice = get_enhanced_advice_sync(
    "600519",
    investment_horizon="medium",  # short, medium, long
    risk_tolerance="moderate"     # conservative, moderate, aggressive
)
```

### 3. 命令行使用

#### 启动服务
```bash
# 启动开发服务器
python stock_advisor_server.py

# 指定端口
python stock_advisor_server.py --host 0.0.0.0 --port 8000
```

#### 运行演示
```bash
# 运行演示脚本
python demo_professional_advice.py

# 选择演示项目
python demo_professional_advice.py --demo basic
```

## API接口

### 获取股票建议
```http
GET /get_stock_advice/{symbol}
```

**参数:**
- symbol: 股票代码 (如: 600519)

**返回示例:**
```json
{
  "symbol": "600519",
  "advice_date": "2024-01-15T10:30:00",
  "current_price": 1678.50,
  "advice": {
    "recommendation": "推荐",
    "action": "买入",
    "confidence": "高",
    "score": 85.5
  },
  "risk_level": {
    "risk_level": "中低风险",
    "risk_color": "绿色",
    "risk_score": 35.2
  },
  "target_prices": {
    "target_price_1m": 1750.00,
    "target_price_3m": 1850.00,
    "stop_loss": 1550.00
  }
}
```

### 获取增强版建议
```http
GET /get_enhanced_advice/{symbol}
```

**参数:**
- symbol: 股票代码
- investment_horizon: 投资期限 (short, medium, long)
- risk_tolerance: 风险偏好 (conservative, moderate, aggressive)

## 配置说明

### 配置文件
项目使用 `config.json` 进行配置，主要配置项包括:

#### 服务器配置
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false,
    "log_level": "INFO",
    "timeout": 30,
    "max_connections": 100
  }
}
```

#### 数据源配置
```json
{
  "data_sources": {
    "eastmoney": {
      "enabled": true,
      "timeout": 10,
      "retry_count": 3,
      "rate_limit": 100
    }
  }
}
```

#### 风险管理配置
```json
{
  "risk_management": {
    "max_position_size": 0.1,
    "stop_loss_percentage": 0.08,
    "take_profit_percentage": 0.15,
    "max_drawdown_threshold": 0.2
  }
}
```

## 部署指南

### 本地部署

#### Windows系统
1. 安装Python 3.8+
2. 克隆项目
3. 运行 `install.bat`
4. 运行 `start_server.py start`

#### Linux/Mac系统
1. 安装Python 3.8+
2. 克隆项目
3. 运行 `chmod +x install.sh && ./install.sh`
4. 运行 `python start_server.py start`

### 云服务器部署

#### 使用Docker
```bash
# 拉取镜像
docker pull mcp-stock-advisor:latest

# 运行容器
docker run -d \
  --name stock-advisor \
  -p 8000:8000 \
  -v /path/to/config:/app/config \
  mcp-stock-advisor:latest
```

#### 使用Docker Compose
```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 反向代理配置

#### Nginx配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 使用示例

### 基础使用
```python
# 获取贵州茅台股票建议
from get_stock_advice import get_stock_advice_sync

advice = get_stock_advice_sync("600519")
print(f"当前价格: ¥{advice['current_price']}")
print(f"投资建议: {advice['advice']['recommendation']}")
print(f"风险等级: {advice['risk_level']['risk_level']}")
```

### 高级使用
```python
# 获取个性化投资建议
from get_enhanced_investment_advice import get_enhanced_advice_sync

advice = get_enhanced_advice_sync(
    "600519",
    investment_horizon="long",
    risk_tolerance="conservative",
    investment_amount=100000
)

# 查看情景分析
bull_scenario = advice['scenario_analysis']['bull_scenario']
print(f"牛市情景目标价: ¥{bull_scenario['price_target']}")
print(f"实现概率: {bull_scenario['probability']}%")
```

### 批量分析
```python
# 批量分析股票
stocks = ["600519", "000858", "601318", "000001"]
results = []

for stock in stocks:
    advice = get_stock_advice_sync(stock)
    results.append({
        "股票": stock,
        "建议": advice['advice']['recommendation'],
        "风险": advice['risk_level']['risk_level']
    })

# 按风险等级排序
results.sort(key=lambda x: x['风险'])
```

## 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2. 端口被占用
```bash
# 检查端口占用
netstat -anp | grep 8000

# 使用其他端口
python start_server.py start --port 8001
```

#### 3. 数据源连接失败
- 检查网络连接
- 确认数据源可用性
- 检查防火墙设置

#### 4. 内存不足
- 减少并发连接数
- 增加缓存超时时间
- 使用轻量级配置

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

## 性能优化

### 缓存配置
```json
{
  "cache": {
    "redis": {
      "enabled": true,
      "host": "localhost",
      "port": 6379,
      "ttl": 300
    }
  }
}
```

### 数据库优化
- 使用连接池
- 添加索引
- 定期清理缓存

## 安全建议

### 生产环境安全
- 使用HTTPS
- 配置防火墙
- 定期更新依赖
- 限制访问IP

### 数据安全
- 加密敏感数据
- 定期备份配置
- 监控异常访问

## 更新维护

### 版本更新
```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重启服务
python start_server.py restart
```

### 备份策略
- 定期备份配置文件
- 备份数据库
- 创建系统快照

## 技术支持

### 获取帮助
- 查看项目Issues
- 提交Bug报告
- 参与社区讨论

### 联系方式
- 项目主页: https://github.com/F415643/stock-advisor-mcp-service
- 问题反馈: https://github.com/F415643/stock-advisor-mcp-service/issues

## 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。