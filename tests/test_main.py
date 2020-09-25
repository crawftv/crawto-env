#!/usr/bin/env python3

import pytest
from src.main import cli

def test_cli(runner,caplog):
    with open("requirements.in", "w"):
        pass
    out = runner.invoke(cli, ["pandas", "numpy"])
    with open("requirements.in", "r") as req:
        requirements = req.read()
        assert "pandas\nnumpy\n" == requirements

def test_cli_repeat(runner,caplog):
    with open("requirements.in", "w"):
        pass
    out = runner.invoke(cli, ["pandas", "numpy"])
    out = runner.invoke(cli, ["pandas", "numpy"])
    with open("requirements.in", "r") as req:
        requirements = req.read()
        assert "pandas\nnumpy\n" == requirements
