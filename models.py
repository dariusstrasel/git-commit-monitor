import requests
from datetime import timedelta, datetime
import os
try:
    import config
except ModuleNotFoundError as error:
    pass



class User:
    """Class object used to represent a user and their repositories."""

    def __init__(self, username, instance_object):
        self.username = username
        self.auth_instance = instance_object
        self.user_repos = []

    def get_user_repositories(self) -> list:
        """Finds a user's repositories from their github account."""
        repo_owner = self.username
        repo_url = 'd' + repo_owner + '/repos'
        parameters = None
        rest_result = self.auth_instance.api_get(repo_url, parameters)
        print([repo_name['full_name'] for repo_name in rest_result])
        if rest_result:
            self.user_repos = [repo_name['name'] for repo_name in rest_result]
        else:
            print("No user repositories found.")
            return []

    @staticmethod
    def split_repository_name(repo_name):
        """Returns a repo name by splicing an input string as such 'username/reponame.'"""
        REPO_NAME = 1
        repo_tokens = repo_name.split('/')
        return repo_tokens[REPO_NAME]

    def get_repository_commits(self, repository_name):
        """Gets the commit history of a repository via the github API."""
        # 2017-05-03T11:30:24.321455
        # test time: 2017-05-01T11:30:24.321455
        # datetime.datetime.now().isoformat()
        repository_owner = self.username
        params = {
            'since': (datetime.today() - timedelta(days=3)).isoformat(),
        }
        repo_commit_url = 'https://api.github.com/repos/' + repository_owner + '/' + repository_name + '/commits'
        result = self.auth_instance.api_get(repo_commit_url, params)
        return result

    def get_user_commit_history(self):
        """Searches a user's github repos and collects/returns their commit history."""
        self.get_user_repositories()
        result = []
        if self.user_repos:
            for repository in self.user_repos:
                result.append(self.get_repository_commits(repository))
            return result
        else:
            return None

    @staticmethod
    def count_repository_commits(repo_commit_results):
        """WIP: """
        len([commit for commit in repo_commit_results])


class Instance:

    def __init__(self):
        self.FILENAME = r'config.py'
        self.auth_enabled = config.gh_auth_enabled

    def initialize_config(self):
        """Create a local filesystem config file for grabbing secret info
         for authenticating on Github's API interface."""
        print("Auth Config not found, creating new one.")
        file = open(self.FILENAME, 'w')
        file.write('"DO NOT ADD TO PUBLIC GIT; CONTAINS SECRETS"')
        file.write('auth = False\n')
        file.write('username = "your_github_username"\n')
        file.write('password = "your_github_password"\n')
        file.close()
        return self.get_user_config()

    def get_user_config(self):
        """Gets the username and password stored in the config.py file and returns as dictionary."""
        if os.path.exists(self.FILENAME):
            if config.gh_auth_enabled:
                user_credentials = {
                    'username': config.username,
                    'password': config.password
                }
                return user_credentials
            else:
                # Auth is disabled within config file.
                return None
        else:
            # Config file does not exist.
            return self.initialize_config()

    @staticmethod
    def split_pagination_link(string):
        link = '<https://api.github.com/user/4576823/repos?page=2>; rel="next", <https://api.github.com/user/4576823/repos?page=2>'
        link_tokens = [item.strip() for item in link.split(',')]
        pages = {token.split(';')[0]: token.split(';')[1].strip() for token in link_tokens}
        return pages
    # TODO: Add pagination module, https://stackoverflow.com/questions/33878019/how-to-get-data-from-all-pages-in-github-api-with-python


    def api_get(self, url, payload):
        """Amorphous API call used to reduce redundant code by creating an interface for input-based API calls."""
        pagination_attribute = "?page{0}&per_page=100"
        mutated_url = url + pagination_attribute
        if self.auth_enabled:
            username = config.username
            password = config.password
            result = requests.get(mutated_url, params=payload, auth=(username, password))
        else:
            result = requests.get(mutated_url, params=payload)
        print("GET ", result.url, payload)
        if result.status_code == 200:
            if result.text == '[]':
                return None
            else:
                return result.json()
        if result.status_code == 403:
            print("Status return '403', the Github API limit is likely being throttled.")
            return None
        else:
            print("API Call returned '%s', not '200' status code." % (result.status_code))
            return None

