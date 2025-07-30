#!/usr/bin/env python3
"""
启动修复后的MCP股票数据服务器
"""

import subprocess
import sys
import os

def main():
    print("🚀 启动修复后的MCP股票数据服务器...")
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_file = os.path.join(current_dir, "stock_advisor_server_fixed.py")
    
    if not os.path.exists(server_file):
        print(f"❌ 找不到服务器文件: {server_file}")
        return
    
    try:
        # 启动服务器
        cmd = [sys.executable, server_file, "--name", "股票数据服务", "--debug"]
        print(f"📡 执行命令: {' '.join(cmd)}")
        
        subprocess.run(cmd, cwd=current_dir)
        
    except KeyboardInterrupt:
        print("\n⏹️  服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()