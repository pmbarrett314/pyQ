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


def simple_get(args):
    token_dict = authenticate(args.email, args.password, args.client_id, args.client_secret)

    url = "https://q.daskeyboard.com/api/1.0/{endpoint}".format(endpoint=args.endpoint)
    headers = make_headers(token_dict["access_token"])

    r = requests.get(url, headers=headers)
    pprint.pprint(json.loads(r.content))


def get_with_pid(args):
    token_dict = authenticate(args.email, args.password, args.client_id, args.client_secret)

    url = "https://q.daskeyboard.com/api/1.0/{pid}/{endpoint}".format(pid=args.pid, endpoint=args.endpoint)
    headers = make_headers(token_dict["access_token"])

    r = requests.get(url, headers=headers)
    pprint.pprint(json.loads(r.content))


def get_signals(args):
    token_dict = authenticate(args.email, args.password, args.client_id, args.client_secret)

    if args.after is not None:
        url = "https://q.daskeyboard.com/api/1.0/signals/after/{after}".format(after=args.after)
    else:
        url = "https://q.daskeyboard.com/api/1.0/signals"
    headers = make_headers(token_dict["access_token"])
    params = {"pid": args.pid}

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

    auth_group = parser.add_argument_group("Authentication info")
    auth_group.add_argument("--client_id", dest='client_id', default=os.getenv("PYQ_CLIENT_ID"),
                            help="client id")
    auth_group.add_argument("--client_secret", dest='client_secret', default=os.getenv("PYQ_CLIENT_SECRET"),
                            help="client secret")
    auth_group.add_argument("--email", dest='email', default=os.getenv("PYQ_EMAIL"),
                            help="email")
    auth_group.add_argument("--password", dest="password", default=os.getenv("PYQ_PASSWORD"), nargs='?',
                            action=PasswordPromptAction,
                            help="password")

    subparsers = parser.add_subparsers()

    auth_parser = subparsers.add_parser('auth', help='auth help')
    auth_parser.set_defaults(func=auth)

    device_definitions_parser = subparsers.add_parser('device_definitions', help='device_definitions help')
    device_definitions_parser.set_defaults(func=simple_get, endpoint="device_definitions")

    devices_parser = subparsers.add_parser('devices', help='devices help')
    devices_parser.set_defaults(func=simple_get, endpoint="devices")

    colors_parser = subparsers.add_parser('colors', help='colors help')
    colors_parser.set_defaults(func=simple_get, endpoint="colors")

    zones_parser = subparsers.add_parser('zones', help='zones help')
    zones_parser.set_defaults(func=get_with_pid, endpoint="zones")
    zones_parser.add_argument("--pid", dest="pid", required=True,
                              help="pid")

    effects_parser = subparsers.add_parser('effects', help='effects help')
    effects_parser.set_defaults(func=get_with_pid, endpoint="effects")
    effects_parser.add_argument("--pid", dest="pid", required=True,
                                help="pid")

    signals_parser = subparsers.add_parser('signals', help='signal help')
    signals_parser.set_defaults(func=get_signals, endpoint="signals")
    signals_parser.add_argument("--pid", dest="pid",
                                help="pid")
    signals_parser.add_argument("--after", dest="after",
                                help="after")

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
