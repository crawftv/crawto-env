#!/usr/bin/env python3

import click
from piptools.scripts.compile import BaseCommand
import os


def check_for_in() -> bool:
    if not os.path.exists("requirements.in"):
        raise Exception("Cannot find requirements.in file")
    return True

class RequirementsInWriter:
    def __init__(self):
        self.dst_file = "requirements.in"

    def write(self,packages):
        with click.open_file(self.dst_file) as requirements_in:
            z = requirements_in.read()
            requirements_in.write(unstyle(z).encode("utf-8"))
            requirements_in.write(os.linesep.encode("utf-8"))
            for package in packages:
                requirements_in.write(unstyle(package).encode("utf-8"))
                requirements_in.write(os.linesep.encode("utf-8"))

@click.command(cls=BaseCommand, context_settings={"help_option_names": ("-h", "--help")})
@click.argument("packages",nargs=-1)
def cli(packages,dst_file):
    check_for_in()
    writer = RequirementsInWriter(dst_file)
    writer.write()
