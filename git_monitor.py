"""
Title: Git Commit Monitor
Author: Darius Strasel strasel.darius@gmail.com
"""

import models
import argparse
import pprint
import random
from twilio_client import main as send_sms


def format_sms_message(commit_length):
    quotes = [
            "“Don’t Let Yesterday Take Up Too Much Of Today.” -Will Rogers",
            "“You Learn More From Failure Than From Success. Don’t Let It Stop You. Failure Builds Character.”- Unknown",
            "“It’s Not Whether You Get Knocked Down, It’s Whether You Get Up.” – Inspirational Quote By Vince Lombardi",
            "“Failure Will Never Overtake Me If My Determination To Succeed Is Strong Enough.”- Og Mandino",
            "“We May Encounter Many Defeats But We Must Not Be Defeated.”- Maya Angelou",
            "“Knowing Is Not Enough; We Must Apply. Wishing Is Not Enough; We Must Do.”- Johann Wolfgang Von Goethe",
            "“Imagine Your Life Is Perfect In Every Respect; What Would It Look Like?”- Brian Tracy",
            "“We Generate Fears While We Sit. We Overcome Them By Action.”- Dr. Henry Link",
            "“The Only Limit To Our Realization Of Tomorrow Will Be Our Doubts Of Today.”- Franklin D. Roosevelt",
            "“Do What You Can With All You Have, Wherever You Are.”- Theodore Roosevelt",
        ]
    commit_dictionary = {
        0: ["Hey! You committed %s times today: aka you didn't commit today. You can do this!",
            "I noticed you didn't commit today! (%s times) You probably noticed too... keep pushing!",
            "You committed %s times today. C'mon! You can do it!"
            ],
        1: ["You committed %s time today. Keep up the good work!",
        "Congrats! You have %s commit for today",
        "Keep it up! You completed %s code commit today!"],
        2: ["You're on a roll! You completed %s commits!", "You committed %s times today. Keep up the good work!",
        "Congrats! You committed %s times today!",
        "Keep it up! You completed %s code commits today!"]
    }
    def pick_message(custom=False):
        if custom:
            message = (random.choice((commit_dictionary[2])) % (custom))
        else:
            message = (random.choice((commit_dictionary[commit_length])) % (commit_length))
        return message
    if commit_length == 0:
        message = pick_message() + random.choice(quotes)
        return message
    else:
        for commit_count in commit_dictionary.keys():
            if commit_count == commit_length:
                message = pick_message()
            else:
                message = pick_message(commit_length)
    return message


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

        data = user.get_user_commit_history()
        commit_length = len(data)
        message = format_sms_message(commit_length)
        send_sms(message)
        #print(data)
        pp.pprint(data)

    else:
        print("No results returned from API.")
        return "No results returned from API."


if __name__ == "__main__":
    main()
