from setuptools import setup

setup(
    name="crawto-env",
    version="1.0.0",
    entry_points={"console_scripts": ["crawto-env=src.main:cli"]},
)
