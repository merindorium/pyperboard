import markdown

from pyperboard.converter import extensions


def convert_md(md_text: str) -> str:
    md = markdown.Markdown(extensions=['extra',
                                       'toc',
                                       'codehilite',
                                       extensions.RestApiExtension(),
                                       extensions.SegmentExtension()])
    html = md.convert(md_text)
    return html
