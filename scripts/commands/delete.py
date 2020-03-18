#!/usr/bin/env python3

import click
import pkg_resources as pr

@click.group()
def delete():
    pass

@delete.command()
def delete():
    """Delete has not yet been implemented and exists only as an example."""
    click.echo('delete was called.')
