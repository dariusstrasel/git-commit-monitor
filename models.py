import requests
import datetime
import pprint
import secrets

"""
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
u'{"type":"User"...'
>>> r.json()
{u'private_gists': 419, u'total_private_repos': 77, ...}
"""


class User:
    """Class object used to represent a user and their repositories."""

    def __init__(self, username):
        self.username = username
        self.user_repos = []

    def get_user_repositories(self) -> list:
        """Finds a user's repositories from their github account."""
        repo_owner = self.username
        repo_url = 'https://api.github.com/users/' + repo_owner + '/repos'
        result = api_get(repo_url, None)
        if result:
            self.user_repos = [self.split_repository_name(repo_name['full_name']) for repo_name in result]
        else:
            return None

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
            'since': datetime.datetime.now().isoformat(),
        }
        repo_commit_url = 'https://api.github.com/repos/' + repository_owner + '/' + repository_name + '/commits'
        result = api_get(repo_commit_url, params)
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


def api_get(url, payload):
    """Amorphous API call used to reduce redundant code by creating an interface for input-based API calls."""
    result = requests.get(url, params=payload)
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
