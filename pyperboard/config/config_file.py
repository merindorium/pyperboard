import yaml

from pyperboard.errors import ConfigError


class ConfigFile:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> dict:
        try:
            with open(self.file_path, "r") as f:
                return yaml.safe_load(f.read())
        except IOError as e:
            raise ConfigError(f"File read error. {e}")
        except yaml.YAMLError:
            raise ConfigError("File parsing error. Please check your YAML config file")
