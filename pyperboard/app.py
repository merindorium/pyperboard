from flask import Flask

from pyperboard import views


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="", static_folder="static")

    app.add_url_rule('/', 'index', views.index_page)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
