import yaml

from pyperboard.cli import printer
from pyperboard.errors import ConfigError


class ConfigFile:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> dict:
        print(f"Reading {self.file_path} config file")
        try:
            with open(self.file_path, "r") as f:
                return yaml.safe_load(f.read())
        except IOError:
            printer.error("File read error")
            raise ConfigError()
        except yaml.YAMLError:
            printer.error("File parsing error. \n\t Please check your YAML config file")
            raise ConfigError()
