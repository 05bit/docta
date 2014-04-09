"""
Command line interface (CLI) for Docta.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *
import os
import docta.project


def main():
    DoctaCLI()
    return 0


HELP_TEXT = """Command line interface (CLI) for Docta.

Commands:

    init    start new docs project in current dir
    config  show project config
    build   build project
    help    show help

More info:
https://github.com/05bit/python-docta
"""


class DoctaCLI(object):
    """Command line interface (CLI) for Docta."""
    def __init__(self):
        self.load_config()
        self.cmd_help()

    def load_config(self):
        self.config = {}

    def cmd_build(self):
        project = docta.project.DoctaProject(os.getcwd(), **self.config)

    def cmd_config(self):
        print(self.config)

    def cmd_help(self):
        print(HELP_TEXT)

    def cmd_init(self):
        raise NotImplemented


if __name__ == '__main__':
    sys.exit(main())
