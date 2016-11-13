"""
Docta projects handler.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import os
import docta.chapters
import docta.exceptions
import docta.render
import docta.utils.fs as fs
import docta.utils.meta as meta

# Defaults
OUT_FORMAT_DEFAULT = 'html'


class Project(object):
    """
    Project data handler: scans project directories, manages resources,
    creates empty project, builds project.
    """
    def __init__(self, path, **config):
        self.path = path
        self.config = config

    def load(self):
        """
        Load project structure.
        """
        self.tree = []

        for chapter_config in self.config.get('chapters', []):
            config = self.config.copy()
            config.update(chapter_config)
            # print("Chapter config: %s" % config)

            nav_path = config.get('base_nav_path', '')
            chapter = docta.chapters.load_tree(self.input_dir(config),
                                              config, nav_path=nav_path)
            self.tree.append(chapter)
            # self.print_tree(self.tree[-1])

    def build(self, formats=None):
        """
        Build project with specified formats.
        """
        self.load()

        for out_format in (formats or [OUT_FORMAT_DEFAULT]):
            render_class = docta.render.get_renderer(out_format)
            renderer = render_class(self)
            renderer.render()

    def input_dir(self, config=None):
        """
        Full input dir path for specified config.
        """
        if config is None:
            config = self.config
        return fs.real(fs.join(self.path, config.get('input_path', '.')))

    def output_dir(self, out_format=None):
        """
        Output directory for specified format.
        """
        output = self.config['output'][out_format]
        if isinstance(output, dict):
            output_rel_path = output.get('build_path', out_format)
        else:
            output_rel_path = output
        return fs.path_for_dir(self.path, output_rel_path)

    def assets_dir(self, out_format=None):
        """
        Output directory for assets and specified format.
        """
        output = self.config['output'][out_format]
        if isinstance(output, dict):
            output_rel_path = output.get('assets_path')
            if output_rel_path:
                return fs.path_for_dir(self.path, output_rel_path)

    def templates_dir(self):
        """
        Jinja templates directory.
        """
        return fs.path_for_dir(self.path, self.config.get('templates', '_templates'))

    def copy_resources(self, out_format=None):
        """
        Copy resources to output directory.
        """
        if self.config.get('resources', None):
            in_resources = fs.path_for_dir(self.path, self.config['resources'])
            out_resources = self.output_dir(out_format)
            fs.cp(in_resources, out_resources, overwrite=True)

    def copy_assets(self, out_format=None):
        """
        Copy assets to output directory.
        """
        if self.config.get('assets', None):
            in_assets = fs.path_for_dir(self.path, self.config['assets'])
            out_assets = self.assets_dir(out_format)
            fs.cp(in_assets, out_assets, overwrite=True)

    def print_tree(self, root):
        """
        DEBUG: print chapters tree
        """
        def print_chapter(chapter, level=0):
            print('  '*level, str(chapter))
            for ch in chapter.children:
                print_chapter(ch, level+1)
        print_chapter(root)

