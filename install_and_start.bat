@echo off
chcp 65001 >nul
echo 🚀 MCP股票数据服务 - 安装和启动脚本
echo ================================================

echo.
echo 📦 第一步：检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    echo 📥 下载地址: https://python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境检查通过

echo.
echo 📦 第二步：安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败，尝试使用国内镜像...
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
)
echo ✅ 依赖包安装完成

echo.
echo 🧪 第三步：测试服务器功能...
python test_fixed_server.py
if errorlevel 1 (
    echo ⚠️  测试发现问题，但将继续启动服务器...
) else (
    echo ✅ 服务器功能测试通过
)

echo.
echo 🚀 第四步：启动MCP服务器...
echo 📡 服务器将在 localhost:8080 启动
echo 💡 按 Ctrl+C 可停止服务器
echo.

python stock_advisor_server_fixed.py --name "股票数据服务" --debug --port 8080

echo.
echo ⏹️  服务器已停止
pause