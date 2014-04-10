"""
Command line interface (CLI) for Docta.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import argparse
import json
import os
import os.path
import docta.project
import sys

CONFIG_FILE = 'docta.conf'
OK_CODE = 0
ERROR_CODE = 2
ERROR_LOGFILE = 'docta-error.log'


def main():
    """
    Run command or show help message.
    """
    try:
        cli = CLI()
        cli.run()
    except Exception as e:
        exit_with_error(e.message)

    cleanup_log()
    return OK_CODE


def exit_with_error(message):
    """
    Show error message and exit with error code.
    """
    sys.stderr.write('Error: %s\n' % message)

    import traceback
    out = open(ERROR_LOGFILE, 'wb')
    out.write('-' * 60 + '\n')
    traceback.print_exc(limit=20, file=out)
    out.write('-' * 60 + '\n')
    out.close()

    sys.exit(ERROR_CODE)


def cleanup_log():
    if os.path.isfile(ERROR_LOGFILE):
        os.unlink(ERROR_LOGFILE)


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Custom arguments parser with nicer error formatting.
    """
    def error(self, message):
        if len(sys.argv) > 1:
            exit_with_error(message)


class CLI(object):
    """
    Command line interface (CLI) for Docta.
    """
    def __init__(self):
        self.init_parser()

    def init_parser(self):
        parser = CustomArgumentParser(description=self.__doc__)
        parser.add_argument('-c', '--config',
                            help='config file to use [default: %(default)s]',
                            default=CONFIG_FILE)
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

        # Command: help
        cmd_help = sub_parsers.add_parser('help',
            help='show this help message and exit')

        self.parser = parser
        self.args = parser.parse_args()

    def run(self):
        if self.args.command:
            getattr(self, 'cmd_%s' % self.args.command)()
        else:
            self.cmd_help()

    def current_dir(self):
        return os.getcwd()

    def current_config(self):
        if not hasattr(self, '_config'):
            config_path = os.path.join(self.current_dir(), self.args.config)
            
            try:
                config_file = open(config_path, 'r')
            except:
                raise Exception("can't load config file: %s" % config_path)

            try:
                self._config = json.load(config_file)
            except Exception as e:
                raise Exception("bad JSON format in config! %s" % e.message)

            config_file.close()

        return self._config

    def current_project(self):
        if not hasattr(self, '_project'):
            self._project = docta.project.Project(self.current_dir(),
                                                       **self.current_config())
        return self._project

    ##
    ## Commands
    ##

    def cmd_build(self):
        self.current_project().build(['html'])

    def cmd_config(self):
        print(json.dumps(self.current_config(), indent=4))

    def cmd_help(self):
        self.parser.print_help()

    def cmd_init(self):
        self.current_project().init()


if __name__ == '__main__':
    sys.exit(main())
