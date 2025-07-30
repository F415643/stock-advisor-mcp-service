>@echo off
REM MCP股票顾问服务 Windows安装脚本

echo.
echo ╔═══════════════════════════════════════╗
echo ║    MCP股票顾问服务安装程序             ║
echo ╚═══════════════════════════════════════╝
echo.

REM 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python 3.9或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到pip，请确保Python安装完整
    pause
    exit /b 1
)

REM 创建虚拟环境
echo 正在创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo 错误: 创建虚拟环境失败
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo 正在升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 正在安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)

REM 创建必要的目录
echo 正在创建必要的目录...
if not exist "logs" mkdir logs
if not exist "data" mkdir data

REM 设置环境变量（可选）
echo 设置环境变量...
set PYTHONPATH=%CD%

REM 测试安装
echo.
echo 正在测试安装...
python -c "import fastmcp; print('FastMCP版本:', fastmcp.__version__)"
if %errorlevel% neq 0 (
    echo 错误: 安装测试失败
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════╗
echo ║    安装完成！                          ║
echo ╚═══════════════════════════════════════╝
echo.
echo 使用方法:
echo 1. 启动服务: python start_server.py
echo 2. 开发模式: python start_server.py --debug
echo 3. 自定义端口: python start_server.py --port 8080
echo.
echo 查看帮助: python start_server.py --help
pause