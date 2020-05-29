import textwrap

import click
import requests

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """Main entrypoint"""
    click.echo("Hello world!")
