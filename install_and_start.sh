#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 MCP股票数据服务 - 安装和启动脚本${NC}"
echo "================================================"

echo ""
echo -e "${BLUE}📦 第一步：检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到Python3，请先安装Python 3.8+${NC}"
    echo -e "${YELLOW}📥 安装方法:${NC}"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

python3 --version
echo -e "${GREEN}✅ Python环境检查通过${NC}"

echo ""
echo -e "${BLUE}📦 第二步：安装依赖包...${NC}"
if ! python3 -m pip install -r requirements.txt; then
    echo -e "${YELLOW}❌ 依赖安装失败，尝试使用国内镜像...${NC}"
    if ! python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt; then
        echo -e "${RED}❌ 依赖安装失败，请检查网络连接${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✅ 依赖包安装完成${NC}"

echo ""
echo -e "${BLUE}🧪 第三步：测试服务器功能...${NC}"
if ! python3 test_fixed_server.py; then
    echo -e "${YELLOW}⚠️  测试发现问题，但将继续启动服务器...${NC}"
else
    echo -e "${GREEN}✅ 服务器功能测试通过${NC}"
fi

echo ""
echo -e "${BLUE}🚀 第四步：启动MCP服务器...${NC}"
echo -e "${YELLOW}📡 服务器将在 localhost:8080 启动${NC}"
echo -e "${YELLOW}💡 按 Ctrl+C 可停止服务器${NC}"
echo ""

# 启动服务器
python3 stock_advisor_server_fixed.py --name "股票数据服务" --debug --port 8080

echo ""
echo -e "${BLUE}⏹️  服务器已停止${NC}"