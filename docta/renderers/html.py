"""
Provides HTML rendered.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *
import docta.renderers.base as base
import docta.fs as fs
import docta.md as md

HTML_INDEX = ('index', 'html')


class Renderer(base.BaseRenderer):
    """
    Renders project to HTML files mirroring source dirs structure.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_name = fs.filename(self.project.index_file())

    def render(self):
        out_format = self.out_format
        input_dir = self.project.input_dir()
        output_dir = self.project.output_dir(out_format)
        input_tree = self.project.input_tree

        # Prepare output dir
        fs.mkdirs(output_dir)

        # Render output files
        for rel_path, files in input_tree:
            fs.mkdirs(fs.path_for_dir(output_dir, rel_path))

            for name in files:
                in_file_path = fs.join(input_dir, rel_path, name)
                out_file_path = fs.join(output_dir, rel_path, self.get_html_name(name))

                with open(out_file_path, 'w') as out_file,\
                     open(in_file_path, 'r') as in_file:
                        html = md.markdown(in_file.read())
                        out_file.write(html)

        # Copy resources
        self.project.copy_resources(out_format)

    def get_html_name(self, name):
        """
        Get .html file name for any other source file name.
        """
        if name == self.index_name:
            bits = (HTML_INDEX[0],)
        else:
            bits = name.rsplit('.', 1)
        return '.'.join((bits[0], HTML_INDEX[1]))
