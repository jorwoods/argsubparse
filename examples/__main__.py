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

    create_subparser(parser, echo)

    parsed = parser.parse_args()
    parsed.func(**vars(parsed))

main()
