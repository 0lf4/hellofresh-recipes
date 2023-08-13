import tomllib
import logging


class AppConfig:
    def __init__(self):
        self._config_file_path = "properties.toml"
        self._config_data = None
        self._load_config()

    def _load_config(self):
        with open(self._config_file_path, "rb") as file:
            self._config_data = tomllib.load(file)

    def get_app_property(self, key):
        if self._config_data and "app" in self._config_data:
            return self._config_data["app"].get(key)
        return None

    def get_database_property(self, key):
        if self._config_data and "database" in self._config_data:
            return self._config_data["database"].get(key)
        return None


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
properties = AppConfig()
