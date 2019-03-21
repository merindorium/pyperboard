import multiprocessing

import click

from pyperboard.cli import Emoji, reporter
from pyperboard.config import ConfigAssembler
from pyperboard.errors import exit_on_error
from pyperboard.renderer import MarkdownRenderer


@click.group()
def cli():
    pass


@cli.command("build")
@exit_on_error
def build_command():
    """Builds static site"""

    reporter.info(f"Starting build... {Emoji.package}")

    config = ConfigAssembler().assemble()

    renderer = MarkdownRenderer(extensions=config.extensions)

    reporter.info("Rendering pages...")
    reporter.info("")

    for page_path in config.pages:
        reporter.success(f"{page_path.split('/')[-1]} rendered")

        with open(page_path, "r") as page:
            print(renderer.render(page.read()))


if __name__ == "__main__":
    cli()
