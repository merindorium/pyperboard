import os
from typing import Any

from marshmallow import EXCLUDE, Schema, fields


class File(fields.String):
    default_error_messages = {"invalid": "{file_name} does not exist"}

    def _validate(self, value: Any) -> None:
        working_dir = os.getcwd()
        file_abs_path = os.path.join(working_dir, value)

        if not os.path.isfile(file_abs_path):
            self.fail("invalid", file_name=value)


class ConfigSchema(Schema):
    pages = fields.List(File, required=True)
    extensions = fields.List(fields.String, missing=[])

    class Meta:
        unknown = EXCLUDE
