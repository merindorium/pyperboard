import os

from pyperboard.utils import Singleton, ROOT_DIR


class Config(metaclass=Singleton):
    DOCS_DIR = None
    THEME = 'default'
    THEMES_DIR = os.path.join(ROOT_DIR, 'themes')

    def update(self, options: dict) -> None:
        for k, v in options.items():
            setattr(self, k, v)
