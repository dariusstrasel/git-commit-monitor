import requests
import datetime
import pprint

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

    def __init__(self, username):
        self.username = username
        self.user_repos = self.get_user_repositories()

    def get_user_repositories(self) -> list:
        repo_owner = self.username
        repo_url = 'https://api.github.com/users/' + repo_owner + '/repos'
        result = api_get(repo_url, None)
        return [self.split_repository_name(repo_name['full_name']) for repo_name in result]

    @staticmethod
    def split_repository_name(repo_name):
        repo_tokens = repo_name.split('/')
        return repo_tokens[1]

    def get_repository_commits(self, repository_name):
        # 2017-05-03T11:30:24.321455
        # datetime.datetime.now().isoformat()
        repository_owner = self.username
        params = {
            'since': '2017-05-01T11:30:24.321455',
        }
        repo_commit_url = 'https://api.github.com/repos/' + repository_owner + '/' + repository_name + '/commits'
        result = api_get(repo_commit_url, params)
        return result

    def return_active_repositories(self, repository_owner):
        repositories = self.get_user_repositories()
        result = []
        for repository in repositories:
            result.append(self.get_repository_commits(repository))
        return result

    @staticmethod
    def process_repository_commits(repo_commit_results):
        len([commit for commit in repo_commit_results])


def api_get(url, payload):
    result = requests.get(url, params=payload)
    print("GET ", result.url, payload)
    if result.status_code == 200:
        if result.text == '[]':
            return None
        else:
            return result.json()
    else:
        print("API Call returned not '200' status code.")
        return None