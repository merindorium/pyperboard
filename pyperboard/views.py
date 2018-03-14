from flask import render_template

from pyperboard.document import Document


def index_page():
    doc = Document('documents/index.md')
    rendered_doc = doc.render()

    return render_template('index.html', DOC=rendered_doc)
