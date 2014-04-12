"""
Docta projects handler.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import os
import docta.chapter
import docta.exceptions
import docta.render
import docta.utils.fs as fs
import docta.utils.meta as meta

# Defaults
INDEX_FILE = docta.chapter.INDEX_FILE
OUT_FORMAT_DEFAULT = 'html'


class Project(object):
    """
    Project data handler: scans project directories, manages resources,
    creates empty project, builds project.
    """
    def __init__(self, path, **config):
        self.path = path
        self.config = config
        self.title = config['title']
        self.logo = config['logo']

    def load(self):
        """
        Load project structure.
        """
        self.tree = [docta.chapter.Chapter.load_tree(self.input_dir(), self.config)]
        self.print_tree()

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

    def print_tree(self):
        """
        DEBUG: print chapters tree
        """
        def print_chapter(chapter, level=0):
            print('  '*level, str(chapter))
            for ch in chapter.children:
                print_chapter(ch, level+1)
        print_chapter(self.tree[0])

