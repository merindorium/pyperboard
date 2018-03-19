from marshmallow import Schema, fields


class ConfigSchema(Schema):
    DOCS_DIR = fields.String(required=True)
