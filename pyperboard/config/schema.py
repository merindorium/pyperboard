from marshmallow import Schema

from pyperboard.config.options import Dir


class ConfigSchema(Schema):
    DOCS_DIR = Dir(required=True)
