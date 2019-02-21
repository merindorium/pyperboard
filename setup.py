from setuptools import setup

setup(
    name="pyperboard",
    entry_points={"console_scripts": ["pyperboard = pyperboard.__main__:cli"]},
)
