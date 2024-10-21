import os
import typer
import functools
from sys import stderr
from json import dumps
from typing import Dict


def print_config(config: Dict) -> str:
    return dumps(config, sort_keys=True, indent=4)

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def require_root(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.geteuid() != 0:
            eprint("Error: This function must be run as root or with sudo")
            raise typer.Exit(code=-1)
        return func(*args, **kwargs)
    return wrapper
