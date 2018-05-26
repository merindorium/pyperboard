import argparse
import logging
import os

import jinja2
import shutil
from pyperboard.config import Config, ConfigurationError
from pyperboard.document import Document

logger = logging.getLogger(__name__)


def local_url_for(endpoint, **values):
    dir_path, file_path = os.path.split(values['filename'])
    dir_path = dir_path[0].replace("/", "./") + dir_path[1:]
    return os.path.join(dir_path, file_path)


def render_locally(config):
    documentation = Document()
    pages = documentation.render()

    current_theme_dir = os.path.join(config.THEMES_DIR, config.THEME)

    d = jinja2.Environment(
        loader=jinja2.FileSystemLoader(f'{current_theme_dir}/templates')
    ).get_template('index.html').render(pages=pages, url_for=local_url_for)

    build_dir = os.path.join(config.DOCS_DIR, '_build')
    index_file_path = os.path.join(build_dir, 'index.html')

    try:
        shutil.rmtree(build_dir)
    except FileExistsError:
        pass

    theme_static_dir = os.path.join(config.THEMES_DIR, config.THEME, 'static')

    shutil.copytree(src=theme_static_dir, dst=build_dir)

    with open(index_file_path, 'w') as f:
        f.write(d)


def build():
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

        docs_dir = os.path.dirname(os.path.abspath(args.config))

        config.DOCS_DIR = docs_dir

        try:
            config.update_from_json(options)
        except ConfigurationError as err:
            for option, errors in err.errors.items():
                logger.error(f"{option}: {errors.pop()}")
        else:
            render_locally(config)


if __name__ == '__main__':
    build()
