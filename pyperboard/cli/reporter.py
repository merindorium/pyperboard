import click
import colorful

colorful.disable()
colorful.use_8_ansi_colors()


class Emoji:
    package = "\U0001F4E6"
    check_mark = "\U00002714"
    cross_mark = "\U00002716"
    info = "\U00002139"


class Reporter:
    def info(self, message: str):
        click.echo(" {} {}\033[K".format(colorful.bold_cyan(Emoji.info), message))

    def error(self, error: str):
        click.echo(f" {colorful.bold_red(Emoji.cross_mark)} {error}", err=True)

    def success(self, message: str):
        click.echo(f" {colorful.bold_green(Emoji.check_mark)} {message}")


reporter = Reporter()
