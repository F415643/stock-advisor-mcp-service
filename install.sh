#!/bin/bash
# MCP股票顾问服务 Linux/macOS安装脚本

set -e  # 遇到错误立即退出

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║    MCP股票顾问服务安装程序             ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python版本
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未检测到Python3，请先安装Python 3.9或更高版本${NC}"
        echo "安装方法:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "  macOS: brew install python3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo -e "${GREEN}检测到Python版本: $PYTHON_VERSION${NC}"
}

# 检查pip
check_pip() {
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}错误: 未检测到pip3${NC}"
        echo "安装方法:"
        echo "  Ubuntu/Debian: sudo apt install python3-pip"
        echo "  CentOS/RHEL: sudo yum install python3-pip"
        exit 1
    fi
}

# 创建虚拟环境
create_venv() {
    echo "正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误: 创建虚拟环境失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}虚拟环境创建成功${NC}"
}

# 激活虚拟环境
activate_venv() {
    echo "正在激活虚拟环境..."
    source venv/bin/activate
    echo -e "${GREEN}虚拟环境已激活${NC}"
}

# 升级pip
upgrade_pip() {
    echo "正在升级pip..."
    python -m pip install --upgrade pip
}

# 安装依赖
install_dependencies() {
    echo "正在安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误: 安装依赖失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}依赖包安装成功${NC}"
}

# 创建必要的目录
create_directories() {
    echo "正在创建必要的目录..."
    mkdir -p logs data
    echo -e "${GREEN}目录创建成功${NC}"
}

# 设置权限
set_permissions() {
    echo "正在设置文件权限..."
    chmod +x start_server.py
    chmod +x install.sh
    echo -e "${GREEN}权限设置完成${NC}"
}

# 测试安装
test_installation() {
    echo "正在测试安装..."
    python -c "import fastmcp; print('FastMCP版本:', fastmcp.__version__)"
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误: 安装测试失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}安装测试通过${NC}"
}

# 主安装流程
main() {
    check_python
    check_pip
    create_venv
    activate_venv
    upgrade_pip
    install_dependencies
    create_directories
    set_permissions
    test_installation
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║    安装完成！                          ${NC}║"
    echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
    echo ""
    echo "使用方法:"
    echo "1. 激活虚拟环境: source venv/bin/activate"
    echo "2. 启动服务: python start_server.py"
    echo "3. 开发模式: python start_server.py --debug"
    echo "4. 自定义端口: python start_server.py --port 8080"
    echo ""
    echo "查看帮助: python start_server.py --help"
}

# 执行主函数
main