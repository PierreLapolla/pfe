import logging
from logging.handlers import QueueHandler, QueueListener
from pathlib import Path
from queue import Queue
import colorlog

class LoggerSingleton:
    """
    Singleton class to initialize and manage the application logger with asynchronous logging support.
    A new log file is created for each application run.
    """
    _instance = None

    def __new__(cls, log_level=logging.INFO) -> 'LoggerSingleton':
        """
        Create a new instance of LoggerSingleton if it doesn't exist.

        :param log_level: The logging level to be set for the logger.
        :return: The singleton instance of LoggerSingleton.
        """
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)

            log_file = Path(f'logs/app.log')
            log_file.parent.mkdir(parents=True, exist_ok=True)
            if log_file.exists():
                log_file.unlink()

            log_queue = Queue()

            cls._instance.logger = logging.getLogger('app_logger')
            cls._instance.logger.setLevel(log_level)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)

            log_format = '%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s'
            formatter = logging.Formatter(log_format)
            file_handler.setFormatter(formatter)

            queue_handler = QueueHandler(log_queue)
            cls._instance.logger.addHandler(queue_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            color_formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
                datefmt=None,
                reset=True,
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
                secondary_log_colors={},
                style='%'
            )
            console_handler.setFormatter(color_formatter)
            cls._instance.logger.addHandler(console_handler)

            listener = QueueListener(log_queue, file_handler)
            listener.start()

            cls._instance.listener = listener

        return cls._instance

    def get_logger(self) -> logging.Logger:
        """
        Get the logger instance.

        :return: The logger instance.
        """
        return self.logger


log = LoggerSingleton(log_level=logging.DEBUG).get_logger()
