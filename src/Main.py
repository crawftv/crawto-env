#!/usr/bin/env python3
import click
from piptools.scripts.compile import BaseCommand
from piptools.logging import log
import os
import platform


class RequirementsInWriter:
    def __init__(self):
        self.dst_file = "requirements.in"

    def check_for_in(self) -> bool:
        if not os.path.exists("requirements.in"):
            with click.open_file(self.dst_file, "w") as requirements_in:
                pass
            return True

    def write(self, packages):
        with click.open_file(self.dst_file, "r") as requirements_in:
            previous_lines = [i.strip("\n") for i in requirements_in.readlines()]

        with click.open_file(
            self.dst_file, "w", atomic=True, lazy=True
        ) as requirements_in:
            for line in previous_lines:
                requirements_in.write(line)
                requirements_in.write("\n")
                log.info(str(line))
            for package in packages:
                if package not in previous_lines:
                    log.info(str(package))
                    requirements_in.write(package)
                    requirements_in.write("\n")


@click.command(
    cls=BaseCommand, context_settings={"help_option_names": ("-h", "--help")}
)
@click.argument("packages", nargs=-1)
def install(packages):
    writer = RequirementsInWriter()
    writer.check_for_in()
    writer.write(packages)
    os.system("pip-compile requirements.in --output-file=requirements.txt")
    os.system("python -m pip install -r requirements.txt")
    return


@click.command(
    cls=BaseCommand, context_settings={"help_option_names": ("-h", "--help")}
)
@click.argument("packages", nargs=-1)
def uninstall(packages):
    if ".crawto-env-config" not in os.listdir():
        raise Exception("Cannot find .crawto-env.config. Please run this in your root directory.")

    with open(".crawto-env-config", "r") as config:
        env_name = config.read()

    os.system(f"virtualenv --clear {env_name}")
    packages = [ i for i in packages ]
    in_packages = []
    with click.open_file("requirements.in", "r") as reqs_in:
        in_packages = [
            i.replace("\n", "")
            for i in reqs_in.readlines()
            if i.replace("\n", "") not in packages
        ]
    with open("requirements.in","w") as blank_file:
        blank_file.write("")
    install(in_packages)
    return

@click.command(
    cls=BaseCommand, context_settings={"help_option_names": ("-h", "--help")}
)
@click.option("-n", "--name", default=".venv")
def create(name):
    cwd = os.getcwd()
    log.info(f"Creating virtual environment in this directory\n{cwd}")
    os.system(f"python -m virtualenv {name}")
    with click.open_file(".crawto-env-config", "w") as config:
        config.write(name)
    log.info("Activating virutal environment")
    platform = platform.system()
    if os_name == "Windows":
        os.system(f"{name}/Scripts/activate")
    elif os_name in ["Linux", "Darwin"]:
        os.system(f"source {name}/bin/activate")

    log.info("Creating requirements.in")
    install(["pip-tools"])
    return


@click.group()
def cli():
    pass


cli.add_command(install)
cli.add_command(create)
cli.add_command(uninstall)
