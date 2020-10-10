#!/usr/bin/env python3

import pytest
from src.main import cli, install, uninstall, create
import os


def test_install(tmpdir, runner, caplog):
    os.chdir(tmpdir)
    with open("requirements.in", "w"):
        pass
    out = runner.invoke(cli, ["install", "pandas", "numpy"])
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



def test_create(tmpdir, runner, ):
    os.chdir(tmpdir)
    out = runner.invoke(
        cli,
        ["create", "-n", ".test_env"]
    )
    assert ".test_env" in os.listdir()
    assert ".crawto-env-config" in os.listdir()

    os.chdir(tmpdir)
    out = runner.invoke(cli, ["create", "--name" ".test_env"])
    assert ".test_env" in os.listdir()
    assert ".crawto-env-config" in os.listdir()

    os.chdir(tmpdir)
    out = runner.invoke(
        cli,
        [
            "create",
        ],
    )
    assert ".venv" in os.listdir()
    assert ".crawto-env-config" in os.listdir()

def test_uninstall(tmpdir, runner,monkeypatch):
    os.chdir(tmpdir)
    runner.invoke(cli, ["create",])
    runner.invoke(cli, ["install", "pandas","numpy"])
    runner.invoke(cli, ["uninstall", "numpy"])
    #uninstall(["numpy"])
    with open("requirements.in", "r") as req:
        requirements = req.read()
        assert "pandas\n" == requirements
