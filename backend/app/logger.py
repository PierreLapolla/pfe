import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            log_file = Path('logs/app.log')
            log_file.parent.mkdir(parents=True, exist_ok=True)

            cls._instance.logger = logging.getLogger('app_logger')
            cls._instance.logger.setLevel(logging.INFO)

            # Create handler that rotates logs after 5MB, keeping 3 backups
            handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
            handler.setLevel(logging.INFO)

            log_format = '%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s'
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)

            cls._instance.logger.addHandler(handler)

        return cls._instance

    def get_logger(self):
        return self.logger


log = LoggerSingleton().get_logger()
