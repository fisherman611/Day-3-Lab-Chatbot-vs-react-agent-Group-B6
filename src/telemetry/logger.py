import logging
import json
import os
from datetime import datetime
from typing import Any, Dict

class IndustryLogger:
    """
    Structured logger that simulates industry practices.
    Logs to both console and a file in JSON format.
    """
    def __init__(self, name: str = "AI-Lab-Agent", log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # File Handler (Human-readable format)
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Thêm handler nếu logger này chưa có handler nào (để tránh trùng lặp)
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        # Quan trọng: Đặt propagate = True để các log từ agent này cũng được gửi lên root logger
        # (giúp chúng xuất hiện trong file log_agent.txt của run_agent.py)
        self.logger.propagate = True

    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Logs an event in a human-readable format."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Header for the event
        header = f"\n[EVENT: {event_type}] @ {timestamp}"
        self.logger.info(header)
        
        # Format the data part prettily
        try:
            # Use indent=2 and ensure_ascii=False for Vietnamese support
            pretty_data = json.dumps(data, indent=2, ensure_ascii=False)
            self.logger.info(pretty_data)
            self.logger.info("-" * 30) # Separator
        except Exception as e:
            self.logger.error(f"Failed to log data: {e}")
            self.logger.info(str(data))

    def info(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str, exc_info=True):
        self.logger.error(msg, exc_info=exc_info)

# Global logger instance
logger = IndustryLogger()
