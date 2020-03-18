import requests
import json
import click
from lib.base import BitBucketAdmin
from lib.exceptions import RepoAlreadyExistsException

class CreateRepo(BitBucketAdmin):
    """CreateRepo Class Goes Here"""
    def __init__(self, login=None, passwd=None, project=None, repo=None, force=False):
        try:
            # Init superclass (BitBucketAdmin)
            super(CreateRepo, self).__init__(login, passwd, project, repo)

        except KeyError:
            print("Required key(s) not defined, or defined incorrectly.")
            raise

        # Convert usernames (for default reviewers) to UUIDs
        self._convert_usernames()
        if self._repo_exists() and force == False:
            click.secho("Repo already exists in bitbucket. Rerun with --force flag to force execution and possibly overwrite.", fg='bright_red')
            raise RepoAlreadyExistsException

    def create_repo(self):
        """Create a repo in bitbucket"""
        click.secho("Creating '{}' repository...".format(self.repo), fg='green', nl=False)
        r = requests.post(
            self.repo_endpoint,
            data = json.dumps(self.merged_config['repo']),
            headers = {'Content-Type': 'application/json'},
            auth = (self.login, self.passwd)
        )
        # Hack-ish way to detect 200/201/204/etc.
        if str(r.status_code).startswith('20'):
            click.secho("done.", fg='green')
        else:
            click.secho("HTTP {}".format(r.status_code), fg='bright_red')

    def create_branch_restrictions(self):
        """Create branching restrictions (eg num of approvals needed to merge to {branch_name}"""
        for k,v in self.merged_config['branch-restrictions'].items():
            if v == None: continue # allow 'null' override
            click.secho("Applying {} restriction...".format(k), fg='green', nl=False)
            r = requests.post(
                f"{self.repo_endpoint}/branch-restrictions",
                data = json.dumps(v),
                headers = {'Content-Type': 'application/json'},
                auth = (self.login, self.passwd)
            )
            if str(r.status_code).startswith('20'):
                click.secho("done.", fg='green')
            else:
                click.secho("HTTP {}".format(r.status_code), fg='bright_red')

    def create_branching_model(self):
        """Create branching _model_ for repo (eg what is bugfix, what is release, etc)"""
        click.secho("Applying branching model...", fg='green', nl=False)
        r = requests.put(
            f"{self.repo_endpoint}/branching-model/settings",
            data = json.dumps(self.merged_config['branching-model']),
            auth = (self.login, self.passwd)
        )
        if str(r.status_code).startswith('20'):
            click.secho("done.", fg='green')
        else:
            click.secho("HTTP {}".format(r.status_code), fg='bright_red')

    def create_default_reviewers(self):
        """Add default reviewers to project"""
        click.secho("Adding default reviewers...", fg='green')
        for userdict in self.merged_config['default-reviewers']:
            # If we couldn't find the UUID earlier its value became None
            if userdict == None: continue
            click.secho("Adding '{}'...".format(userdict['username']), fg='green', nl=False)
            r = requests.put(
                f"{self.repo_endpoint}/default-reviewers/{userdict['uuid']}",
                headers = {'Content-Type': 'application/json'},
                data = '{"foo":"bar"}', # This api endpoint requires data but doesn't actually use it.
                auth = (self.login, self.passwd)
            )
            if str(r.status_code).startswith('20'):
                click.secho("done.", fg='green')
            else:
                click.secho("HTTP {}".format(r.status_code), fg='bright_red')

    def enable_pipelines(self):
        """Enables (or disables) pipelines for a repo"""
        click.secho("Enabling pipelines...", fg='green', nl=False)
        r = requests.put(
            f"{self.repo_endpoint}/pipelines_config",
            headers = {'Content-Type': 'application/json'},
            data = json.dumps(self.merged_config['pipelines-config']),
            auth = (self.login, self.passwd)
        )
        if str(r.status_code).startswith('20'):
            click.secho("done.", fg='green')
        else:
            click.secho("HTTP {}".format(r.status_code), fg='bright_red')

    def create_pipelines_environments(self):
        """Create environments to be used by pipelines"""
        for env,details in self.merged_config['pipelines-environments'].items():
            click.secho("Creating '{}' environment...".format(env), fg='green', nl=False)
            r = requests.post(
                f"{self.repo_endpoint}/environments/",
                headers = {'Content-Type': 'application/json'},
                data = json.dumps(details),
                auth = (self.login, self.passwd)
            )
            if str(r.status_code).startswith('20'):
                click.secho("done.", fg='green')
            else:
                click.secho("HTTP {}".format(r.status_code), fg='bright_red')

    def purge_existing_environments(self):
        """Delete existing pipelines environments (enabling creates defaults)"""
        existing_envs = requests.get(
            f"{self.repo_endpoint}/environments/",
            headers = {'Content-Type': 'application/json'},
            auth = (self.login, self.passwd)
        )
        for env in existing_envs.json()['values']:
            click.secho("Purging existing '{}' environment...".format(env['name']), fg='bright_magenta', nl=False)
            r = requests.delete(
                f"{self.repo_endpoint}/environments/{env['uuid']}",
                headers = {'Content-Type': 'application/json'},
                auth = (self.login, self.passwd)
            )
            if str(r.status_code).startswith('20'):
                click.secho("done.", fg='bright_magenta')
            else:
                click.secho("HTTP {}".format(r.status_code), fg='bright_red')
