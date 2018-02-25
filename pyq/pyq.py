import argparse
import getpass
import json
import os
import pprint
import requests

from authentication import authenticate


def make_headers(access_token, post=False):
    headers = {
        "Authorization": "Bearer {access_token}".format(access_token=access_token),
    }
    if post:
        headers["Content-Type"] = "application/json"
    return headers


def auth(args):
    token_dict = authenticate(args.email, args.password, args.client_id, args.client_secret)
    pprint.pprint(token_dict)


def signal(args):
    print("hello signal")


def device_definitions(args):
    token_dict = authenticate(args.email, args.password, args.client_id, args.client_secret)

    url = "https://q.daskeyboard.com/api/1.0/device_definitions"
    headers = make_headers(token_dict["access_token"])

    r = requests.get(url, headers=headers)
    pprint.pprint(json.loads(r.content))


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

    device_definition_parser = subparsers.add_parser('device_definitions', help='device_definitions help')
    device_definition_parser.set_defaults(func=device_definitions)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
