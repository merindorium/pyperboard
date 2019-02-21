import os

from marshmallow.exceptions import ValidationError

from pyperboard.cli import printer
from pyperboard.config.base import Config
from pyperboard.config.config_file import ConfigFile
from pyperboard.config.schema import ConfigSchema
from pyperboard.errors import ConfigError


class ConfigAssembler:
    CONFIG_FILENAME = ".pyperboard"
    CONFIG_EXT = ["yml", "yaml"]

    def assemble(self) -> Config:
        config_file_path = self._get_config_file_path()

        config_file = ConfigFile(file_path=config_file_path)
        config_raw_data = config_file.read()

        config_data = self._load_config_data(config_raw_data)

        config = Config()
        config.update(config_data)

        printer.info("Config successfully loaded")
        return config

    def _get_config_file_path(self) -> str:
        current_dir = os.getcwd()

        for ext in self.CONFIG_EXT:
            filename = f"{self.CONFIG_FILENAME}.{ext}"
            path = os.path.join(current_dir, filename)

            if os.path.isfile(path):
                return path

        printer.error("No config file")
        raise ConfigError()

    def _load_config_data(self, raw_data: dict) -> dict:
        try:
            return ConfigSchema().load(raw_data)
        except ValidationError as e:
            self._process_validation_errors(errors=e.messages)
            raise ConfigError()

    def _process_validation_errors(self, errors: dict) -> None:
        printer.error("Config file error")
        for field, error in errors.items():
            printer.error(f"Parameter - {field} --- {error}")
