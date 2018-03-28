import os

from pyperboard.config.schema import ConfigSchema
from pyperboard.utils import Singleton, ROOT_DIR


class ConfigurationError(Exception):
    def __init__(self, errors: dict):
        self.errors = errors


class Config(metaclass=Singleton):
    DOCS_DIR = None
    THEME = 'default'
    THEMES_DIR = os.path.join(ROOT_DIR, 'themes')
    ORDER = []

    def update_from_json(self, json_data: str) -> None:
        options, errors = ConfigSchema().loads(json_data)

        if errors:
            raise ConfigurationError(errors=errors)

        self._update(options)

    def _update(self, options: dict) -> None:
        for k, v in options.items():
            setattr(self, k, v)
