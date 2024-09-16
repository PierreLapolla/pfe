import os
from pathlib import Path
from typing import Any, Optional, Union

import yaml

from .logger import log


class ConfigSingleton:
    """
    Singleton class to load and manage configuration from a YAML file and environment variables.

    :param file_path: The path to the configuration YAML file.
    :type file_path: Union[str, Path]
    """
    _instance = None

    def __new__(cls, file_path: Union[str, Path]):
        """
        Create a new instance of ConfigSingleton if it doesn't exist.

        :param file_path: The path to the configuration YAML file.
        :type file_path: Union[str, Path]
        :return: The singleton instance of ConfigSingleton.
        :rtype: ConfigSingleton
        """
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            cls._instance.config = {}
            config_file = Path(file_path)

            if config_file.is_file():
                with open(config_file, 'r') as file:
                    cls._instance.config = yaml.safe_load(file) or {}
            else:
                log.error(f"config file '{config_file}' not found")

            cls._instance._merge_env_variables()

        return cls._instance

    def __call__(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Get a configuration value by key.

        :param key: The configuration key.
        :type key: str
        :param default: The default value to return if the key is not found.
        :type default: Optional[Any]
        :return: The configuration value or the default value if the key is not found.
        :rtype: Optional[Any]
        """
        return self.config.get(key, default)

    def _merge_env_variables(self):
        """
        Override configuration values with environment variables where applicable.
        """
        for key in self.config:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                log.info(f"overriding config key '{key}' with value from environment variable '{key.upper()}'")
                self.config[key] = env_value

        for key, value in os.environ.items():
            if key.upper() not in self.config:
                log.info(f"adding environment variable '{key}' to config")
                self.config[key.upper()] = value


config = ConfigSingleton('config.yaml')
