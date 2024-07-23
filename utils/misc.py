from sys import stderr
from json import dumps
from typing import Dict


def print_config(config: Dict) -> str:
    return dumps(config, sort_keys=True, indent=4)


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
