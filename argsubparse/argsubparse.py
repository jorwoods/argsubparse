import argparse
import inspect

from typing import Callable, Mapping, Sequence


def create_subparser(parser: argparse.ArgumentParser, func: Callable,
                     short_options: Mapping[str, str],
                     skip_args: Sequence = list(),
                     subparser_name = None,
                     ) -> argparse.ArgumentParser:
    '''
    Given an existing argparse ArgumentParser, and a function to be exposed as
    a command line interface, this function will inspect the passed function
    and build a subparser for it. The intention being that it should reduce
    duplication of argument declaration while making use of tools existing
    in the standard library.
    '''
    try:
        subparser = [action for action in parser._actions
                     if isinstance(action, argparse._SubParsersAction)][0]
    except IndexError:
        subparser = parser.add_subparsers()
    function_parser = subparser.add_parser(subparser_name or func.__name__)

    existing_actions = set(action.dest for action in parser._actions)
    existing_actions = existing_actions.union(('args', 'kwargs'))
    skips = existing_actions.union(skip_args)

    signature = inspect.signature(func)
    for k, v in signature.parameters:  
        arg_params = dict()
        if k in skips:
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

    function_parser.usage = func.__doc__
    function_parser.set_defaults(func=func)

    return function_parser
