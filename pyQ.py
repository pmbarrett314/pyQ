import argparse


def auth(args):
    print("hello auth")


def signal(args):
    print("hello signal")


def main():
    parser = argparse.ArgumentParser(description="Send a notification to your 5Q.")
    subparsers = parser.add_subparsers()

    auth_parser = subparsers.add_parser('auth', help='auth help')
    auth_parser.set_defaults(func=auth)

    signal_parser = subparsers.add_parser('signal', help='signal help')
    signal_parser.set_defaults(func=signal)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
