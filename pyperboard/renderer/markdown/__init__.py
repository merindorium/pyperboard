import markdown

from pyperboard.renderer import base
from pyperboard.renderer.markdown import extensions


class MarkdownRenderer(base.Renderer):
    def render(self, page: str) -> str:
        return self.markdown_renderer.convert(page)

    @property
    def markdown_renderer(self) -> markdown.Markdown:
        return markdown.Markdown(
            extensions=[
                "extra",
                "toc",
                "codehilite",
                extensions.RestApiExtension(),
                extensions.SegmentExtension(),
            ]
        )
