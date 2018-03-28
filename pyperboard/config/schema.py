from marshmallow import Schema, fields

from pyperboard.config import options


class ConfigSchema(Schema):
    DOCS_DIR = options.Dir(required=True)
    ORDER = fields.List(fields.String())
