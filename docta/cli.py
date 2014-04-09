"""
Command line interface (CLI) for Docta.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *
import argparse
import json
import os
import os.path
import docta.project
import sys

OK_CODE = 0
ERROR_CODE = 2


def main():
    try:
        DoctaCLI()
    except Exception as e:
        exit_with_error(e.message)
    return OK_CODE


def exit_with_error(message):
    """
    Show error message and exit with error code.
    """
    sys.stderr.write('Error: %s\n' % message)
    sys.exit(ERROR_CODE)    


class DoctaArgParser(argparse.ArgumentParser):
    """
    Custom arguments parser with nicer error formatting.
    """
    def error(self, message):
        if len(sys.argv) > 1:
            exit_with_error(message)


class DoctaCLI(object):
    """
    Command line interface (CLI) for Docta.
    """
    def __init__(self):
        self.init_parser()
        self.init_config()
        self.run()

    def init_parser(self):
        parser = DoctaArgParser(description=self.__doc__)
        parser.add_argument('-c', '--config', help='config file to use [default: %(default)s]',
                            default='docta.conf')
        sub_parsers = parser.add_subparsers(dest='command')

        # Command: init
        cmd_init = sub_parsers.add_parser('init',
            help='start new docs project in current directory')

        # Command: config
        cmd_config = sub_parsers.add_parser('config',
            help='test and show project config')

        # Command: build
        cmd_build = sub_parsers.add_parser('build',
            help='build project')

        # Command: build
        cmd_help = sub_parsers.add_parser('help',
            help='show this help message and exit')

        self.parser = parser
        self.args = parser.parse_args()

    def init_config(self):
        config_path = os.path.join(self.current_dir(), self.args.config)
        config_file = open(config_path, 'r')
        self.config = json.load(config_file)
        config_file.close()

    def run(self):
        if self.args.command:
            getattr(self, 'cmd_%s' % self.args.command)()
        else:
            self.cmd_help()

    def current_dir(self):
        return os.getcwd()

    def current_project(self):
        if not getattr(self, '_project', None):
            self._project = docta.project.DoctaProject(self.current_dir(), **self.config)
        return self._project

    def cmd_build(self):
        project = self.current_project()
        project.build()

    def cmd_config(self):
        print(json.dumps(self.config, indent=4))
        # def _line(k, v, level=0):
        #     if isinstance(v, dict):
        #         for _k, _v in v.items():
        #             _line(_k, _v, level+1)
        #     else:
        #         print("%s%s => %s" % ('  ' * level, k, v))
        # _line(None, self.config, level=-1)

    def cmd_help(self):
        self.parser.print_help()

    def cmd_init(self):
        project = self.current_project()
        project.init()


if __name__ == '__main__':
    sys.exit(main())
