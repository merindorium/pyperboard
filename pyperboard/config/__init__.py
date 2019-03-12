import os

from marshmallow.exceptions import ValidationError

from pyperboard.cli import reporter
from pyperboard.config.base import Config
from pyperboard.config.config_file import ConfigFile
from pyperboard.config.schema import ConfigSchema
from pyperboard.errors import ConfigError


class ConfigAssembler:
    CONFIG_FILENAME = ".pyperboard"
    CONFIG_EXT = ["yml", "yaml"]

    def assemble(self) -> Config:
        reporter.info("Prepearing configuration...")
        config_file_path = self._get_config_file_path()

        config_file = ConfigFile(file_path=config_file_path)

        reporter.info(f"Reading config file")
        config_raw_data = config_file.read()

        config_data = self._load_config_data(config_raw_data)

        config = Config()
        config.update(config_data)

        reporter.success("Config loaded successfully")

        return config

    def _get_config_file_path(self) -> str:

        for ext in self.CONFIG_EXT:
            filename = f"{self.CONFIG_FILENAME}.{ext}"
            path = os.path.join(self.current_working_dir, filename)

            if os.path.isfile(path):
                return path

        raise ConfigError("No config file")

    @property
    def current_working_dir(self) -> str:
        return os.getcwd()

    def _load_config_data(self, raw_data: dict) -> dict:
        try:
            return ConfigSchema().load(raw_data)
        except ValidationError:
            raise ConfigError("Config is invalid")
