#!/usr/bin/env python3
"""
MCP股票顾问服务启动脚本
提供多种启动方式和配置选项
"""

import os
import sys
import argparse
import logging
import asyncio
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stock_advisor_server import StockAdvisorServer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('stock_advisor.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='启动MCP股票顾问服务')
    
    parser.add_argument(
        '--host', 
        default='0.0.0.0', 
        help='服务器主机地址 (默认: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8000, 
        help='服务器端口 (默认: 8000)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true', 
        help='启用调试模式'
    )
    
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
        default='INFO',
        help='日志级别 (默认: INFO)'
    )
    
    parser.add_argument(
        '--config', 
        type=str, 
        help='配置文件路径'
    )
    
    parser.add_argument(
        '--mode', 
        choices=['dev', 'prod', 'test'], 
        default='dev',
        help='运行模式 (默认: dev)'
    )
    
    return parser.parse_args()

def setup_logging(log_level: str, debug: bool = False):
    """设置日志配置"""
    level = getattr(logging, log_level.upper())
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level if not debug else logging.DEBUG)
    
    # 清除现有处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level if not debug else logging.DEBUG)
    
    # 创建文件处理器
    file_handler = logging.FileHandler('stock_advisor.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def load_config(config_path: str = None) -> dict:
    """加载配置文件"""
    config = {
        'host': '0.0.0.0',
        'port': 8000,
        'debug': False,
        'log_level': 'INFO',
        'rate_limit': 100,
        'timeout': 30,
        'max_connections': 100,
        'cors_origins': ['*'],
        'api_keys': {},
        'data_sources': {
            'eastmoney': {'enabled': True, 'timeout': 10},
            'tonghuashun': {'enabled': True, 'timeout': 10},
            'xueqiu': {'enabled': True, 'timeout': 10}
        }
    }
    
    if config_path and os.path.exists(config_path):
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
            logger.info(f"加载配置文件: {config_path}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
    
    return config

def check_dependencies():
    """检查依赖项"""
    required_packages = [
        'fastmcp',
        'aiohttp',
        'asyncio',
        'typing',
        'datetime',
        'logging'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少依赖包: {', '.join(missing_packages)}")
        logger.info("请运行: pip install -r requirements.txt")
        return False
    
    return True

def print_startup_banner(host: str, port: int, mode: str):
    """打印启动横幅"""
    banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    MCP股票顾问服务启动                        ║
╠═══════════════════════════════════════════════════════════════╣
║  服务地址: http://{host}:{port}                                 ║
║  运行模式: {mode.upper()}                                       ║
║  日志文件: stock_advisor.log                                  ║
║  文档地址: http://{host}:{port}/docs                          ║
║  健康检查: http://{host}:{port}/health                        ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def create_pid_file():
    """创建PID文件"""
    try:
        pid = os.getpid()
        with open('stock_advisor.pid', 'w') as f:
            f.write(str(pid))
        logger.info(f"创建PID文件: {pid}")
    except Exception as e:
        logger.warning(f"创建PID文件失败: {e}")

def remove_pid_file():
    """删除PID文件"""
    try:
        if os.path.exists('stock_advisor.pid'):
            os.remove('stock_advisor.pid')
            logger.info("删除PID文件")
    except Exception as e:
        logger.warning(f"删除PID文件失败: {e}")

async def start_server(args, config):
    """启动服务器"""
    try:
        # 创建服务器实例
        server = StockAdvisorServer(
            host=args.host,
            port=args.port,
            debug=args.debug,
            config=config
        )
        
        # 启动服务器
        await server.start()
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
    except Exception as e:
        logger.error(f"启动服务器失败: {e}")
        raise

def main():
    """主函数"""
    try:
        # 解析参数
        args = parse_arguments()
        
        # 检查依赖
        if not check_dependencies():
            sys.exit(1)
        
        # 设置日志
        setup_logging(args.log_level, args.debug)
        
        # 加载配置
        config = load_config(args.config)
        
        # 更新配置
        config['host'] = args.host
        config['port'] = args.port
        config['debug'] = args.debug
        config['mode'] = args.mode
        
        # 创建PID文件
        create_pid_file()
        
        # 打印启动横幅
        print_startup_banner(args.host, args.port, args.mode)
        
        # 记录启动信息
        logger.info(f"启动MCP股票顾问服务 - 模式: {args.mode}")
        logger.info(f"监听地址: {args.host}:{args.port}")
        logger.info(f"调试模式: {args.debug}")
        
        # 启动服务器
        asyncio.run(start_server(args, config))
        
    except KeyboardInterrupt:
        logger.info("服务被用户中断")
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        sys.exit(1)
    finally:
        # 清理
        remove_pid_file()
        logger.info("服务已停止")

if __name__ == "__main__":
    main()