import os
import logging
from logging.handlers import TimedRotatingFileHandler

def init_daily_logger(
    log_dir: str = "logs",
    log_file_name: str = "app.log",
    backup_count: int = 7,
    level: int = logging.INFO,
):
    """
    初始化按天切换的日志记录器，可在 FastAPI 的 startup 中调用。

    Args:
        log_dir: 日志目录
        log_file_name: 日志文件名（默认写入 app.log，切换为 app.log.YYYY-MM-DD）
        backup_count: 保留的历史日志天数
        level: 日志等级（默认 logging.INFO）
    """
    os.makedirs(log_dir, exist_ok=True)

    # 清除旧的 handler，防止重复添加
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # 构造日志路径
    log_file_path = os.path.join(log_dir, log_file_name)

    # 设置按天切换的文件日志处理器
    file_handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when="midnight",        # 每天午夜切换
        interval=1,
        backupCount=backup_count,
        encoding="utf-8",
        utc=False,
    )
    file_handler.suffix = "%Y-%m-%d"  # 切换后的日志文件格式为 app.log.2025-08-05

    # 格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 重新配置日志
    logging.basicConfig(
        level=level,
        handlers=[file_handler, console_handler],
    )

    # init_daily_logger()