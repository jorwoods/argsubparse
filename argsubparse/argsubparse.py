import argparse
import inspect

from typing import Callable, Mapping, Optional, Sequence, Set


def create_subparser(
    parser: argparse.ArgumentParser,
    func: Callable,
    short_options: Mapping[str, str] = dict(),
    skip_args: Sequence = list(),
    subparser_name: Optional[str] = None,
    parents: Set[argparse.ArgumentParser] = set(),
) -> argparse.ArgumentParser:
    '''
    Given an existing argparse ArgumentParser, and a function to be exposed as
    a command line interface, this function will inspect the passed function
    and build a subparser for it. The intention being that it should reduce
    duplication of argument declaration while making use of tools existing
    in the standard library.

    Parameters
    --------------

    parser: An existing argparse.ArgumentParser instance

    func: A function that you wish to add as a subparser for access from
    commandline

    short_options: A Mapping of argument name to the short option names.

    skip_args: A Sequence of arguments to not build flags and options
    for. args and kwargs are always skipped.

    subparser_name: Optionally a name to override the function name from
    command line.

    parents: A Set of ArgumentParser classes to add the arguments to the
    subparser. Adds the parser (first argument) as a parent automatically.
    '''
    try:
        subparser = [action for action in parser._actions
                     if isinstance(action, argparse._SubParsersAction)][0]
    except IndexError:
        subparser = parser.add_subparsers()
    function_parser = subparser.add_parser(subparser_name or func.__name__,
                                           parents=parents)

    skip_args = set(skip_args)
    for parent in parents:
        for action in parent._actions:
            if isinstance(action, argparse._StoreAction):
                skip_args.add(action)

    signature = inspect.signature(func)
    for k, v in signature.parameters.items():
        arg_params = dict()
        if k in skip_args:
            continue
        if v.default is inspect._empty:
            arg_name = (k, )
        else:
            arg_params['default'] = v.default
            short_option = short_options.get(k)
            if short_option is None:
                arg_name = (f'--{k}', )
            else:
                if not short_option.startswith('-'):
                    short_option = f'-{short_option}'
                arg_name = (short_option, f'--{k}')

        if v.annotation is not inspect._empty:
            arg_params['type'] = v.annotation
        function_parser.add_argument(*arg_name, **arg_params)

    function_parser.usage = '\n'.join([parser.usage, func.__doc__])
    function_parser.set_defaults(func=func)

    return function_parser
