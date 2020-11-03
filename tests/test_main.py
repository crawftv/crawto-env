#!/usr/bin/env python3

import pytest
from src.main import cli, install, uninstall, create
import os


def test_install(tmpdir, runner):
    os.chdir(tmpdir)
    with open("requirements.in", "w"):
        pass
    runner.invoke(cli, ["install", "pandas", "numpy"])
    with open("requirements.in", "r") as req:
        requirements = req.read()
        assert "pandas\nnumpy\n" == requirements
    assert "requirements.txt" in os.listdir()


def test_install_repeat(tmpdir, runner, caplog):
    os.chdir(tmpdir)
    with open("requirements.in", "w"):
        pass
    out = runner.invoke(cli, ["install", "pandas", "numpy"])
    out = runner.invoke(cli, ["install", "pandas", "numpy"])
    with open("requirements.in", "r") as req:
        requirements = req.read()
        assert "pandas\nnumpy\n" == requirements


@pytest.mark.parametrize(
    "commands,solution",
    [
        (["create", "-n", "test_env"], "test_env"),
        (["create", "--name", "test_env"], "test_env"),
        (["create"], ".venv"),
    ],
)
def test_create(tmpdir, runner, commands, solution):
    os.chdir(tmpdir)
    runner.invoke(cli, commands)
    assert solution in os.listdir()
    assert ".crawto-env-config" in os.listdir()
    assert ".dev-requirements.in" in os.listdir()


def test_uninstall(tmpdir, runner):
    os.chdir(tmpdir)
    runner.invoke(cli, ["create"])
    runner.invoke(cli, ["install", "pandas", "numpy"])
    runner.invoke(cli, ["uninstall", "numpy"])
    # uninstall(["numpy"])
    with open("requirements.in", "r") as req:
        requirements = req.read()
        assert "pandas\n" == requirements
