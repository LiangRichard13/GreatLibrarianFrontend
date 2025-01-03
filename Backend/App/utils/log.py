# @Author:LiXiang
# @Time:2025/1/3 15:06
import logging
import os
import re
from datetime import datetime

# 正则表达式匹配 ANSI 转义序列
ansi_escape_pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def filter_ansi_escape(text):
    """过滤掉文本中的 ANSI 转义序列"""
    return ansi_escape_pattern.sub('', text)


class ANSIFilter(logging.Filter):
    """自定义日志过滤器，用于过滤 ANSI 转义序列"""

    def filter(self, record):
        record.msg = filter_ansi_escape(record.msg)
        if isinstance(record.args, dict):
            for key in record.args:
                if isinstance(record.args[key], str):
                    record.args[key] = filter_ansi_escape(record.args[key])
        elif isinstance(record.args, (tuple, list)):
            record.args = tuple(filter_ansi_escape(arg) if isinstance(arg, str) else arg for arg in record.args)
        return True


# 配置日志
def setup_logging():
    # 创建日志文件夹（如果不存在）
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # 设置日志文件路径
    log_file = os.path.join(log_dir, f'GLF_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename=log_file,  # 日志文件路径
        level=logging.INFO,  # 日志级别（INFO 及以上级别会被记录）
        format=log_format,  # 日志格式
        filemode='a'  # 追加模式
    )

    # 添加 ANSI 过滤器
    for handler in logging.root.handlers:
        handler.addFilter(ANSIFilter())

    # 如果需要同时输出到控制台，可以添加一个 StreamHandler
    console_handler = logging.StreamHandler()  # 创建一个 StreamHandler 对象，用于将日志输出到控制台
    console_handler.setLevel(logging.INFO)  # 设置控制台日志的级别为 INFO
    console_handler.setFormatter(logging.Formatter(log_format))  # 设置控制台日志的格式
    logging.getLogger().addHandler(console_handler)  # 将控制台处理器添加到根日志记录器