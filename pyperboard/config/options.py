from marshmallow import fields, ValidationError
import os


class Dir(fields.String):
    def _validate(self, value):
        super()._validate(value)

        if not os.path.isdir(value):
            raise ValidationError(f'File {value} not exists')
