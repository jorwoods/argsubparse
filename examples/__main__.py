import argparse
from argsubparse import create_subparser


def echo(data, *args, **kwargs):
    '''
    Prints data to stdout
    '''
    print(data)


def sign_in(server, username, password):
    print('Signed into {} as {}'.format(
        server, username
    ))

def main():
    parser = argparse.ArgumentParser('argsubparse_example')
    parser.add_subparsers(required=True)

    auth_args = argparse.ArgumentParser(add_help=False)
    group = auth_args.add_argument_group('Authentication', )
    tokens = group.add_argument_group('Token Authentication')
    tokens.add_argument('--token_name')
    tokens.add_argument('--token_secret')

    upw_auth = group.add_argument_group('User/Password Authentication')
    upw_auth.add_argument('--username')
    upw_auth.add_argument('--password')

    create_subparser(parser, echo)
    create_subparser(parser, sign_in, parents={auth_args})

    parsed = parser.parse_args()
    parsed.func(**vars(parsed))


main()
