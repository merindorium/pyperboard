import logging

import colorful

stream = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
stream.setFormatter(formatter)

log = logging.getLogger("pyperboard")
log.addHandler(stream)
log.setLevel(logging.DEBUG)


class Printer:
    def info(self, text: str) -> None:
        log.info(self.with_leading(text))

    def heading(self, text: str) -> str:
        heading_text = colorful.bold(text)
        self.info(heading_text)

    def error(self, text: str) -> None:
        error_text = "{} {}".format(colorful.bold_red("Err:"), text)
        log.error(self.with_leading(error_text))

    @staticmethod
    def with_leading(text: str) -> str:
        text_with_leading = "{} {}".format(colorful.bold_purple("--->"), text)
        return text_with_leading


class Emoji:
    @property
    def package(self):
        return "\U0001F4E6"


printer = Printer()
emoji = Emoji()
