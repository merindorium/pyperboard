import logging

import click

from pyperboard.cli import emoji, printer
from pyperboard.config import ConfigAssembler
from pyperboard.errors import exit_on_error


@click.group()
def cli():
    pass


@cli.command("build")
@exit_on_error
def build_command():
    """Builds static site"""

    printer.heading(f"{emoji.package} Starting build...")

    ConfigAssembler().assemble()


if __name__ == "__main__":
    cli()
