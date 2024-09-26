import os
from pathlib import Path
from typing import Any, Optional, Union

import yaml

from .logger import log


class ConfigSingleton:
    """
    Singleton class to load and manage configuration from a YAML file and environment variables.
    """
    _instance = None

    def __new__(cls, file_path: Optional[Union[str, Path]] = None) -> 'ConfigSingleton':
        """
        Create a new instance of ConfigSingleton if it doesn't exist.

        :param file_path: The path to the configuration YAML file.
        :return: The singleton instance of ConfigSingleton.
        """
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            cls._instance.config = {}

            if file_path is not None:
                config_file = Path(file_path)
                if config_file.is_file():
                    with open(config_file, 'r') as file:
                        cls._instance.config = yaml.safe_load(file) or {}
                else:
                    log.error(f"config file '{config_file}' not found")

            cls._instance._merge_env_variables()

        return cls._instance

    def __call__(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value by key.

        :param key: The configuration key.
        :param default: The default value to return if the key is not found.
        :return: The configuration value or the default value if the key is not found.
        """
        if key not in self.config and default is None:
            log.error(f"config key '{key}' not found and no default value provided")
            raise KeyError(f"config key '{key}' not found and no default value provided")

        var = self.config.get(key, default)

        if var is None:
            log.warning(f"config key '{key}' not found, using default value")

        return var

    def _merge_env_variables(self) -> None:
        """
        Override configuration values with environment variables where applicable.

        :return: None
        """
        for key in self.config:
            env_value = os.getenv(key)
            if env_value is not None:
                log.debug(f"overriding config key '{key}' with value from environment variable '{key}'")
                self.config[key] = env_value

        for key, value in os.environ.items():
            if key not in self.config:
                log.debug(f"adding environment variable '{key}' to config")
                self.config[key] = value


config = ConfigSingleton('config.yaml')
