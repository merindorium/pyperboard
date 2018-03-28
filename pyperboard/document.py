import codecs
import logging
import os
from typing import List

from pyperboard.config import Config
from pyperboard.converter import converter

logger = logging.getLogger(__name__)


class Document:
    def __init__(self):
        self.path = Config().DOCS_DIR
        self.pages = []

        self._add_pages()

    def render(self) -> List[str]:
        document_html = []

        for page in self.pages:
            document_html.append(page.render())

        return document_html

    def _add_pages(self) -> None:
        for page_name in Config().ORDER:
            page_path = f'{self.path}/{page_name}'
            if not os.path.exists(page_path):
                logger.warning(f'ORDER: File {page_path} does not exist')
                continue

            new_page = Page(page_path)
            self.pages.append(new_page)


class Page:
    def __init__(self, path: str):
        self.path = path

    def render(self) -> str:
        with codecs.open(self.path, 'r', encoding='utf-8') as f:
            page_html = converter.convert_md(f.read())
        return page_html
