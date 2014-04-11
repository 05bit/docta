"""
Docta projects handler.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import os
import docta.exceptions
import docta.render
import docta.utils.fs as fs
import docta.utils.meta as meta

# Defaults
INDEX_FILE = 'index.md'
OUT_FORMAT_DEFAULT = 'html'


class Project(object):
    """
    Project data handler: scans project directories, manages resources,
    creates empty project, builds project.
    """
    def __init__(self, path, **config):
        self.path = path
        self.config = config
        self.input_tree = []
        self.title = config['title']
        self.logo = config['logo']

    def load(self):
        """
        Load project structure.

        Loads `self.input_tree` as a list of tuples:

            [
                ((str) relative path1, (list) files1, (dict) files meta1),
                ((str) relative path2, (list) files2, (dict) files meta2),
                ...
            ]
        """
        self.input_tree = []

        input_dir = self.input_dir()
        for dir_path, sub_dirs, files in os.walk(input_dir):
            files_to_render = self.files_to_render(files)
            if files_to_render:
                rel_path = dir_path.replace(input_dir, '', 1).strip(fs.sep)
                if not self.is_relpath_masked(rel_path):
                    files_meta = self.files_meta(dir_path, files_to_render)
                    self.input_tree.append((rel_path, files_to_render, files_meta))

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

    def templates_dir(self):
        return fs.path_for_dir(self.path, self.config.get('templates', '_templates'))

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

    def files_meta(self, dir_path, files):
        """
        Extract specified files meta from specified dir path.
        """
        files_meta = {}
        for name in files:
            with open(fs.join(dir_path, name), 'r') as in_file:
                files_meta[name] = meta.extract(in_file)
                # TODO: make page path
                # files_meta[name]['path'] = ...
        return files_meta

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
        out_resources = self.output_dir(out_format)
        for name in os.listdir(in_resources):
            resource_src = fs.join(in_resources, name)
            resource_dst = fs.join(out_resources, name)
            fs.rm(resource_dst, ignore_errors=True)
            fs.cp(resource_src, resource_dst)
