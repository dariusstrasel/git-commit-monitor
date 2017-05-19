"""
Title: Git Commit Monitor
Author: Darius Strasel strasel.darius@gmail.com
"""

import models
import argparse
import pprint


def parse_input_commands():
    parser = argparse.ArgumentParser(prog='Git Commit Monitor',
                                     description='Get the commit history of a user for the past day.')
    parser.add_argument('username', metavar='github-username', type=str,
                        help='a github username')
    # Turn input arguments into dictionary.
    args = vars(parser.parse_args())
    return args


def main():
    """Process input arguments, get user config settings,
     create User/Instance class instances, and get the commit history for the user.
     """
    # Get input arguments, create api instance (checks for secrets info)
    input_arguments = parse_input_commands()
    auth_instance = models.Instance()

    queried_user = input_arguments['username']

    # Create User instance and pass in CLI user, followed by an auth instance
    user = models.User(queried_user, auth_instance)
    user.get_user_repositories()

    pp = pprint.PrettyPrinter(indent=4)

    if user.user_repos:
        pp.pprint(user.get_user_commit_history())
        #print(user.get_user_commit_history())
    else:
        print("No results returned from API.")


if __name__ == "__main__":
    main()
