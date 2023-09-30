import logging
import os
import tomllib


class AppConfig:
    """
    This class is responsible for loading the properties.toml file and
    overriding the values with environment variables.
    """
    def __init__(self):
        self._config_file_path = "server/properties.toml"
        self._config_data = None
        self._load_config()
        self._override_with_env_vars()

    def _load_config(self):
        with open(self._config_file_path, "rb") as file:
            self._config_data = tomllib.load(file)

    def _override_with_env_vars(self):
        for key, value in os.environ.items():
            if key.startswith('APP_'):
                stripped_key = key[4:]
                if "APP" not in self._config_data:
                    self._config_data["APP"] = {}
                self._config_data["APP"][stripped_key] = value

        for key, value in os.environ.items():
            if key.startswith('DB_'):
                stripped_key = key[3:]
                if "DATABASE" not in self._config_data:
                    self._config_data["DATABASE"] = {}
                self._config_data["DATABASE"][stripped_key] = value

    def get_app_property(self, key):
        if self._config_data and "APP" in self._config_data:
            return self._config_data["APP"].get(key)
        return None

    def get_database_property(self, key):
        if self._config_data and "DATABASE" in self._config_data:
            return self._config_data["DATABASE"].get(key)
        return None


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
properties = AppConfig()
