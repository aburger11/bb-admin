#!/usr/bin/env python3

import click
import pkg_resources as pr
import lib.create as c
import os


@click.group()
def create():
    pass

@create.command()
@click.option('-l','--login',
                help="Bitbucket cloud login - eg yourname@socialsolutions.com")
@click.option('--password', prompt=True, hide_input=True, hidden=True)
@click.option('-p','--project',required=True,
                help="Project string in Bitbucket this repo will belong to (eg DATA for 360 Data Pipeline, DO for devops)")
@click.option('-r', '--repo',required=True,
                help="The name (eg cops-bb-admin) to create")
@click.option('-f', '--force', is_flag=True, default=False,
                help="Force execution if repo already exists in BitBucket")
def create(login, password, project, repo, force):
    """Command on cli1"""
    repo = c.CreateRepo(
        login=login,
        passwd=password,
        project=project,
        repo=repo,
        force=force
    )
    repo.create_repo()
    repo.create_branch_restrictions()
    repo.create_branching_model()
    repo.create_default_reviewers()
    repo.enable_pipelines()
    repo.purge_existing_environments()
    repo.create_pipelines_environments()
