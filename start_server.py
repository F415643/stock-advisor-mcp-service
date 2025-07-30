#!/usr/bin/env python3
"""
MCP股票顾问服务启动脚本
提供多种启动方式和配置选项
"""

import argparse
import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """检查依赖项"""
    required_packages = [
        'fastmcp',
        'aiohttp',
        'pandas',
        'numpy',
        'requests',
        'beautifulsoup4'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("需要Python 3.8或更高版本")
        return False
    return True

def setup_environment():
    """设置环境变量"""
    env_vars = {
        'PYTHONPATH': os.path.dirname(os.path.abspath(__file__)),
        'MCP_LOG_LEVEL': os.getenv('MCP_LOG_LEVEL', 'INFO'),
        'MCP_DEBUG': os.getenv('MCP_DEBUG', 'false')
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value

def start_dev_server(host='0.0.0.0', port=8000, debug=False):
    """启动开发服务器"""
    print("启动MCP股票顾问服务开发模式...")
    print(f"服务器地址: http://{host}:{port}")
    
    try:
        from stock_advisor_server import main
        main(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

def start_prod_server(host='0.0.0.0', port=8000):
    """启动生产服务器"""
    print("启动MCP股票顾问服务生产模式...")
    print(f"服务器地址: http://{host}:{port}")
    
    try:
        import uvloop
        import asyncio
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass
    
    try:
        from stock_advisor_server import main
        main(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

def start_docker_server():
    """启动Docker容器"""
    print("使用Docker启动MCP股票顾问服务...")
    
    try:
        # 检查Docker是否安装
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
        
        # 构建镜像
        print("构建Docker镜像...")
        subprocess.run(['docker', 'build', '-t', 'mcp-stock-advisor', '.'], check=True)
        
        # 启动容器
        print("启动Docker容器...")
        subprocess.run([
            'docker', 'run', '-d', '--name', 'mcp-stock-advisor',
            '-p', '8000:8000', 'mcp-stock-advisor'
        ], check=True)
        
        print("Docker容器已启动")
        print("访问地址: http://localhost:8000")
        
    except subprocess.CalledProcessError as e:
        print(f"Docker启动失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("未找到Docker，请先安装Docker")
        sys.exit(1)

def stop_docker_server():
    """停止Docker容器"""
    print("停止Docker容器...")
    
    try:
        subprocess.run(['docker', 'stop', 'mcp-stock-advisor'], check=True)
        subprocess.run(['docker', 'rm', 'mcp-stock-advisor'], check=True)
        print("Docker容器已停止")
    except subprocess.CalledProcessError:
        print("容器已停止或不存在")

def show_status():
    """显示服务状态"""
    print("检查MCP股票顾问服务状态...")
    
    # 检查Python进程
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'stock_advisor_server.py'],
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(f"Python进程运行中 (PID: {result.stdout.strip()})")
        else:
            print("Python进程未运行")
    except FileNotFoundError:
        print("无法检查Python进程状态")
    
    # 检查Docker容器
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mcp-stock-advisor'],
            capture_output=True,
            text=True
        )
        if 'mcp-stock-advisor' in result.stdout:
            print("Docker容器运行中")
        else:
            print("Docker容器未运行")
    except FileNotFoundError:
        print("Docker未安装")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='MCP股票顾问服务启动脚本')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'dev', 'docker', 'install'],
                       help='执行的操作')
    parser.add_argument('--host', default='0.0.0.0', help='服务器主机地址')
    parser.add_argument('--port', type=int, default=8000, help='服务器端口')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    # 检查环境
    if not check_python_version():
        sys.exit(1)
    
    if args.action in ['start', 'dev', 'docker']:
        if not check_dependencies():
            sys.exit(1)
    
    setup_environment()
    
    if args.action == 'start':
        start_prod_server(host=args.host, port=args.port)
    elif args.action == 'dev':
        start_dev_server(host=args.host, port=args.port, debug=args.debug)
    elif args.action == 'docker':
        if len(sys.argv) > 2 and sys.argv[2] == 'stop':
            stop_docker_server()
        else:
            start_docker_server()
    elif args.action == 'stop':
        stop_docker_server()
    elif args.action == 'restart':
        stop_docker_server()
        time.sleep(2)
        start_docker_server()
    elif args.action == 'status':
        show_status()
    elif args.action == 'install':
        print("安装依赖...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("安装完成")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("使用方法:")
        print("  python start_server.py start [--host HOST] [--port PORT]")
        print("  python start_server.py dev [--host HOST] [--port PORT] [--debug]")
        print("  python start_server.py docker [stop]")
        print("  python start_server.py status")
        print("  python start_server.py install")
    else:
        main()