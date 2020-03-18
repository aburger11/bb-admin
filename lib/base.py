import os
import yaml
import requests
import json
import click
import sys
from deepmerge import always_merger

class BitBucketAdmin:
    """BitBucketAdmin Superclass Goes Here"""
    def __init__(self, login=None, passwd=None, project=None, repo=None):
        try:
            self.login   = login
            self.passwd  = passwd
            self.project = project.lower()
            self.repo    = repo
            self.merged_config = self.merge_configs()
            self.repo_endpoint = f"{self.merged_config['global']['bb_api_base_endpoint']}/repositories/{self.merged_config['global']['workspace']}/{repo}"

        except KeyError:
            print("Required key(s) not defined, or defined incorrectly.")
            raise

        self._verify_auth()     # Does this user work?
        self._verify_admin()    # Is this user an admin?

    def _repo_exists(self):
        """Check whether or not a repo exists in bitbucket"""
        r = requests.get(
            self.repo_endpoint,
            auth = (self.login, self.passwd)
        )
        return r.status_code == 200

    def _verify_admin(self):
        """Make sure our user is an admin."""
        try:
            r = requests.get(
                f"{self.merged_config['global']['bb_api_base_endpoint']}/user/permissions/teams",
                auth = (self.login, self.passwd)
            )
            # "permissions" dict exists within an array, so check all elements.
            if not any(a['permission'] == 'admin' for a in r.json()['values']):
                raise
        except:
            click.secho("User does not appear to be an admin.", fg='bright_red')
            sys.exit(1)

    def _verify_auth(self):
        """Make sure our user can authenticate."""
        try:
            r = requests.get(
                f"{self.merged_config['global']['bb_api_base_endpoint']}/user",
                auth = (self.login, self.passwd)
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            click.secho("API returned 401. Is your password incorrect?", fg='bright_red')
            print(e)
            sys.exit(1)

    def merge_configs(self):
        """Merge global and project-level config yamls"""
        root_dir = os.path.abspath(os.path.dirname(__file__))
        global_yaml_path  = os.path.join(root_dir, '../config/socialsolutions.yml')
        project_yaml_path = os.path.join(root_dir, '../config/{0}/{0}.yml'.format(self.project))
        with open(global_yaml_path) as global_file:
            self.global_config = yaml.load(global_file, Loader=yaml.FullLoader)
        with open(project_yaml_path) as project_file:
            self.project_config = yaml.load(project_file, Loader=yaml.FullLoader)

        merged_config = always_merger.merge(self.global_config, self.project_config)

        return merged_config

    def _convert_usernames(self):
        """Converts usernames to UUIDs in-place"""
        for i, user in enumerate(self.merged_config['default-reviewers']):
            click.secho("Getting UUID for user '{}'".format(user), fg='green')
            try:
                r = requests.get(
                    f"{self.merged_config['global']['bb_api_base_endpoint']}/users/{user}",
                    auth = (self.login, self.passwd)
                )
                account_id = r.json()['account_id']
                self.merged_config['default-reviewers'][i] = {}
                self.merged_config['default-reviewers'][i]['username'] = user
                self.merged_config['default-reviewers'][i]['uuid'] = account_id
            except KeyError:
                click.secho("Could not convert '{}' to a UUID.".format(user), fg='bright_red')
                self.merged_config['default-reviewers'][i] = None
        # Now remove duplicates via weird list comprehension
        # Credit: https://www.geeksforgeeks.org/python-removing-duplicate-dicts-in-list/
        self.merged_config['default-reviewers'] = [
            i for n, i in enumerate(self.merged_config['default-reviewers'])
            if i not in self.merged_config['default-reviewers'][n + 1:]
        ]
