import argparse
import sys

from . import decide, search, table
from .common import RecipeError


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Local FDE recipes: table, decide, search. Python standard library only.')
    sub = parser.add_subparsers(dest='recipe', required=True)
    for name, function in [('table', table.run), ('decide', decide.run)]:
        cmd = sub.add_parser(name)
        cmd.add_argument('input')
        cmd.add_argument('--config', required=True)
        cmd.add_argument('--out', required=True, help='New output directory; existing directories are preserved.')
        cmd.set_defaults(function=function)
    cmd = sub.add_parser('search')
    cmd.add_argument('docs')
    cmd.add_argument('--query', required=True)
    cmd.add_argument('--out', required=True)
    cmd.add_argument('--top', type=int, default=3)
    cmd.add_argument('--min-score', type=float, default=0.0)
    cmd.set_defaults(function=search.run)
    args = parser.parse_args(argv)
    try:
        path = args.function(args)
    except (RecipeError, OSError, UnicodeError, ValueError, TypeError, KeyError, ArithmeticError) as exc:
        print(f'Recipe failed: {exc}', file=sys.stderr)
        return 2
    print(f'Created {path}. Read result.json and manifest.json; generation is not independent verification.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
