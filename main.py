"""
Title: Git Commit Monitor
Author: Darius Strasel strasel.darius@gmail.com
"""

import models
import argparse
import pprint


def main():
    parser = argparse.ArgumentParser(prog='Git Commit Monitor', description='Get the commit history of a user for the past day.')
    parser.add_argument('username', metavar='github-username', type=str,
                        help='a github username')
    args = vars(parser.parse_args())
    user_auth = models.Instance.get_config()
    user = models.User(args['username'], user_auth)
    user.get_user_repositories()

    pp = pprint.PrettyPrinter(indent=4)

    if user.user_repos:
        return pp.pprint(len(user.get_user_commit_history()))
    else:
        print("No results returned from API.")


if __name__ == "__main__":
    main()
