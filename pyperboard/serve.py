import argparse
import logging
import os

from flask import Flask

from pyperboard import views
from pyperboard.config import Config, ConfigurationError

logger = logging.getLogger(__name__)


def create_app(config: Config) -> Flask:
    current_theme_dir = os.path.join(config.THEMES_DIR, config.THEME)

    app = Flask(__name__,
                static_url_path="",
                static_folder=f"{current_theme_dir}/static",
                template_folder=f'{current_theme_dir}/templates')

    app.add_url_rule('/', 'index', views.index_page)

    return app


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Path to json config file', type=str, required=True)

    args = parser.parse_args()

    try:
        with open(args.config, 'r') as config_file:
            options = config_file.read()
    except IOError as e:
        logger.error(f'Config file {e.filename} not found.')
        exit(1)
    else:
        config = Config()

        try:
            config.update_from_json(options)
        except ConfigurationError as err:
            for option, errors in err.errors.items():
                logger.error(f"{option}: {errors.pop()}")
        else:
            server = create_app(config)
            server.run()


if __name__ == '__main__':
    serve()
