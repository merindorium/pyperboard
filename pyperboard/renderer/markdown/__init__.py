import markdown

from pyperboard.renderer import base
from pyperboard.renderer.markdown import extensions


class MarkdownRenderer(base.Renderer):

    CUSTOM_EXTENSIONS_MAPPING = {
        "rest_api": extensions.RestApiExtension(),
        "segment": extensions.SegmentExtension(),
    }

    def render(self, page: str) -> str:
        return self.markdown_renderer.convert(page)

    @property
    def markdown_renderer(self) -> markdown.Markdown:
        return markdown.Markdown(extensions=self.extensions)
