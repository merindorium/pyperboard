import codecs

from pyperboard.converter import converter


class Document:
    def __init__(self, path: str):
        self.path = path

    def render(self) -> str:
        with codecs.open(self.path, 'r', encoding='utf-8') as f:
            html = converter.convert_md(f.read())
        return html
