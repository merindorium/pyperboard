import os

from flask import render_template

from pyperboard.config.base import Config
from pyperboard.document import Document


def index_page():
    config = Config()
    docs = []

    for root, dirs, files in os.walk(f'{config.DOCS_DIR}'):
        for file in files:
            if file.endswith(".md"):
                doc = Document(os.path.join(root, file)).render()
                docs.append(doc)

    return render_template('index.html', DOCS=docs)
