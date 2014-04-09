"""
Docta projects handler.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *
import os
import docta.exceptions

# Defaults
INDEX_FILE = 'index.md'
OUT_FORMAT = 'html'

# Shortcuts
os_join = os.path.join
os_real = os.path.realpath
os_dir = os.path.dirname
os_sep = os.path.sep
os_mkdirs = lambda p: os.makedirs(p, mode=0755)
os_mkdirs_noerr = docta.exceptions.suppress(OSError, IOError)(os_mkdirs)


def path_for_file(base, relative):
    """Get real directory path by base dir and relative file path."""
    return os_real(os_dir(os_join(base, relative)))


def path_for_dir(base, relative):
    """Get real directory path by base dir and relative dir path."""
    return os_real(os_join(base, relative))


class Project(object):
    """
    Project data handler: scans project directories, manages resources,
    creates output directories, creates empty project, builds project.
    """
    def __init__(self, path, **config):
        self.path = path
        self.config = config
        self.input_tree = []

    def load(self):
        """
        Load project structure.

        Loads `self.input_tree` as a list of tuples:

            [
                ((str) relative path1, (list) files1),
                ((str) relative path2, (list) files2),
                ...
            ]
        """
        self.input_tree = []

        input_dir = self.input_dir()
        for path, subdirs, files in os.walk(input_dir):
            to_render = self.files_to_render(files)
            if to_render:
                rel_path = path.replace(input_dir, '', 1).strip(os_sep)
                if not self.is_relpath_masked(rel_path):
                    self.input_tree.append((rel_path, to_render))

    def build(self, formats=None):
        """
        Build project with specified formats.
        """
        self.load()

        input_dir = self.input_dir()
        for out_format in (formats or [OUT_FORMAT]):
            # TODO: here we should pick a renderer for format!
            #       But now we'll just perform raw render.
            output_dir = self.output_dir(out_format)
            os_mkdirs_noerr(output_dir)

            output_tree = []
            for rel_path, files in self.input_tree:
                os_mkdirs_noerr(path_for_dir(output_dir, rel_path))

                for name in files:
                    in_file_path = os_join(input_dir, rel_path, name)
                    out_file_path = os_join(output_dir, rel_path, name)
                    print('%s => %s' % (in_file_path, out_file_path))

    def init(self):
        """
        Init empty project.
        """
        raise Exception(NotImplemented)

    def output_dir(self, out_format=None):
        """
        Output directory for specified format.
        """
        return path_for_dir(self.path, self.config['output'][out_format])

    def input_dir(self):
        """
        Input dir based on project index file.
        """
        return path_for_file(self.path, self.config.get('index', INDEX_FILE))

    def files_to_render(self, files):
        """
        Get list of files to render.
        """
        to_render = []
        for name in files:
            if self.is_file_to_render(name):
                to_render.append(name)
        return to_render

    def create_output_dir(self, out_format=None):
        """
        Create output directory if doesn't exist.
        """
        os_mkdirs_noerr(self.output_dir(out_format))

    def is_relpath_masked(self, relative):
        """
        Checks if relative dir path is masked (not rendered) in build.
        """
        for name in relative.strip(os_sep).split(os_sep):
            if self.is_name_masked(name):
                return True
        return False

    def is_name_masked(self, name):
        """
        Checks if file/dir name is masked.
        """
        return name.startswith('_')

    def is_file_to_render(self, name):
        """
        Checks if file is to render.
        """
        if not self.is_name_masked(name):
            if name.endswith('.md'):
                return True
        return False

    def copy_resources(self, out_format=None):
        """
        Copy resources to output directory.
        """
        raise Exception(NotImplemented)
