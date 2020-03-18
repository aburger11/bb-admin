#!/usr/bin/env python3

import click
import pkg_resources as pr
from .commands.create import create
from .commands.delete import delete

@click.group()
@click.version_option(pr.get_distribution('bb-admin').version, '--version', '-v')
def cli():
    pass

cli.add_command(create)
cli.add_command(delete)
