import argparse
from argsubparse import create_subparser


def echo(data, *args, **kwargs):
    '''
    Prints data to stdout
    '''
    print(data)

def main():
    parser = argparse.ArgumentParser('argsubparse_example')
    parser.add_subparsers(required=True)

    group = parser.add_argument_group('Authentication', )
    tokens = group.add_argument_group('Token Authentication')
    tokens.add_argument('--token_name')
    tokens.add_argument('--token_secret')

    upw_auth = group.add_argument_group('User/Password Authentication')
    upw_auth.add_argument('--username')
    upw_auth.add_argument('--password')

    create_subparser(parser, echo)

    parsed = parser.parse_args()
    parsed.func(**vars(parsed))

main()
