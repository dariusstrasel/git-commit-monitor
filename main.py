import requests
import json
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


def get_user_repos(repo_owner):
    repo_url = 'https://api.github.com/users/' + repo_owner + '/repos'
    result = api_get(repo_url, None)
    return [split_repo_name(repo_name['full_name']) for repo_name in result]


def split_repo_name(repo_name):
    repo_tokens = repo_name.split('/')
    return repo_tokens[1]

def get_repo_commits(repository_owner, repository_name):
    # 2017-05-03T11:30:24.321455
    # datetime.datetime.now().isoformat()
    params = {
        'since': '2017-05-01T11:30:24.321455',
    }
    repo_commit_url = 'https://api.github.com/repos/' + repository_owner + '/' + repository_name + '/commits'
    result = api_get(repo_commit_url, params)
    return result

