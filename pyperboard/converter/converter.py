import markdown


def convert_md(md_text: str) -> str:
    html = markdown.markdown(md_text, extensions=['extra', 'toc', 'codehilite'])
    return html
