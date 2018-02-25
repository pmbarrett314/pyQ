import argparse
import getpass
import os
import pprint

from authentication import authenticate


def auth(args):
    token_dict = authenticate(args.email, args.password, args.client_id, args.client_secret)
    pprint.pprint(token_dict)


def signal(args):
    print("hello signal")


class PasswordPromptAction(argparse.Action):
    def __call__(self, parser, args, value, option_string=None):
        if value is not None:
            setattr(args, self.dest, value)
        else:
            setattr(args, self.dest, getpass.getpass())


def main():
    parser = argparse.ArgumentParser(description="Send a notification to your 5Q.")
    subparsers = parser.add_subparsers()

    auth_parser = subparsers.add_parser('auth', help='auth help')
    auth_parser.set_defaults(func=auth)

    auth_parser.add_argument("--client_id", dest='client_id', default=os.getenv("PYQ_CLIENT_ID"),
                             help="client id")
    auth_parser.add_argument("--client_secret", dest='client_secret', default=os.getenv("PYQ_CLIENT_SECRET"),
                             help="client secret")
    auth_parser.add_argument("--email", dest='email', default=os.getenv("PYQ_EMAIL"),
                             help="email")
    auth_parser.add_argument("--password", dest="password", default=os.getenv("PYQ_PASSWORD"), nargs='?',
                             action=PasswordPromptAction,
                             help="password")

    signal_parser = subparsers.add_parser('signal', help='signal help')
    signal_parser.set_defaults(func=signal)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
