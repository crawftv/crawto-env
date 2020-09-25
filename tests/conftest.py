#!/usr/bin/env python3

from click.testing import CliRunner
import pytest


@pytest.fixture
def runner():
    cli_runner = CliRunner(mix_stderr=False)
    yield cli_runner
