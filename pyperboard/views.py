from flask import render_template

from pyperboard.document import Document


def index_page():
    documentation = Document()
    pages = documentation.render()

    return render_template('index.html', pages=pages)
