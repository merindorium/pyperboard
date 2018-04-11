import markdown

from pyperboard.converter import extensions

md = markdown.Markdown(extensions=['extra',
                                   'toc',
                                   'codehilite',
                                   extensions.RestApiExtension()])


def convert_md(md_text: str) -> str:
    html = md.convert(md_text)
    return html
