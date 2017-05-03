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

    user = models.User(args['username'])


    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(user.get_user_commit_history())

if __name__ == "__main__":
    main()