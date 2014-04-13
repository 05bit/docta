"""
Command line interface (CLI) for Docta.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import argparse
import os
import sys
import docta.project
import docta.utils.server
import docta.utils.json as json
import docta.utils.fs as fs
import docta.utils.log as log

CONFIG_FILE = 'docta.conf'
OK_CODE = 0
ERROR_CODE = 2


def main():
    """
    Run command or show help message.
    """
    try:
        cli = CLI()
        cli.run()
    except Exception as exc:
        message = getattr(exc, 'message', str(exc))
        exit_with_error(message, exc=exc)

    log.cleanup()
    return OK_CODE


def exit_with_error(message, exc=None):
    """
    Show error message and exit with error code.
    """
    log.error(message)
    if exc:
        log.traceback()
    sys.exit(ERROR_CODE)


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

        # Command: serve
        cmd_help = sub_parsers.add_parser('serve',
            help='start local server for testing')

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

    def script_name(self):
        return fs.basename(sys.argv[0])

    def current_config(self):
        if not hasattr(self, '_config'):
            config_path = fs.join(self.current_dir(), self.args.config)
            
            try:
                config_file = open(config_path, 'r')
            except:
                raise Exception("can't load config file: %s" % config_path)

            try:
                self._config = json.load(config_file)
            except Exception as e:
                raise Exception("bad JSON format in config! %s" % log.exc_to_str(e))

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
        import docta

        # test if dir is empty
        for name in os.listdir(self.current_dir()):
            if not name.startswith('.'):
                command = ' '.join((self.script_name(), self.args.command))
                exit_with_error("Current dir is not empty. Please run `%s` in empty dir." % command)

        # copy initial project
        source_dir = fs.real(fs.dirname(docta.__file__))
        initial_dir = fs.join(source_dir, 'initial', 'default')
        fs.cp(initial_dir, self.current_dir())

    def cmd_serve(self):
        project = self.current_project()
        path = project.output_dir('html')
        port = project.config['server']['port']
        docta.utils.server.run(path, port=port)


if __name__ == '__main__':
    sys.exit(main())
