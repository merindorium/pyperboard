from pyperboard.cli import reporter


class PyperboardError(Exception):
    pass


class ConfigError(PyperboardError):
    pass


def exit_on_error(func):
    def decorator():
        try:
            func()
        except PyperboardError as e:
            reporter.error(e)
            exit(1)

    return decorator
