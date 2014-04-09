"""
Docta projects handler.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import super
import os
import shutil
import docta.exceptions
import docta.render
import docta.utils.fs as fs

# Defaults
INDEX_FILE = 'index.md'
OUT_FORMAT_DEFAULT = 'html'
OUT_RESOURCES_DIR = 'static'


class Project(object):
    """
    Project data handler: scans project directories, manages resources,
    creates empty project, builds project.
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
                rel_path = path.replace(input_dir, '', 1).strip(fs.sep)
                if not self.is_relpath_masked(rel_path):
                    self.input_tree.append((rel_path, to_render))

    def build(self, formats=None):
        """
        Build project with specified formats.
        """
        self.load()

        for out_format in (formats or [OUT_FORMAT_DEFAULT]):
            render_class = docta.render.get_renderer(out_format)
            renderer = render_class(self)
            renderer.render()

    def init(self):
        """
        Init empty project.
        """
        raise Exception(NotImplemented)

    def output_dir(self, out_format=None):
        """
        Output directory for specified format.
        """
        return fs.path_for_dir(self.path, self.config['output'][out_format])

    def input_dir(self):
        """
        Input dir based on project index file.
        """
        return fs.dirname(self.index_file())

    def index_file(self):
        """
        Get full path for main index file.
        """
        return fs.real(fs.join(self.path, self.config.get('index', INDEX_FILE)))

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
        fs.mkdirs(self.output_dir(out_format))

    def is_relpath_masked(self, relative):
        """
        Checks if relative dir path is masked (not rendered) in build.
        """
        for name in relative.strip(fs.sep).split(fs.sep):
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
        in_resources = fs.path_for_dir(self.path, self.config.get('resources', '_resources'))
        out_resources = fs.path_for_dir(self.output_dir(out_format), OUT_RESOURCES_DIR)
        shutil.rmtree(out_resources, ignore_errors=True)
        shutil.copytree(in_resources, out_resources)
