"""
Provides HTML rendered.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *
import docta.renderers.base as base
import docta.fs as fs


class Renderer(base.BaseRenderer):
    """
    Renders project to HTML files mirroring source dirs structure.
    """
    def render(self):
        out_format = self.out_format
        input_dir = self.project.input_dir()
        output_dir = self.project.output_dir(out_format)
        input_tree = self.project.input_tree

        # Prepare output dir
        fs.mkdirs_noerr(output_dir)

        # Render output files
        for rel_path, files in input_tree:
            fs.mkdirs_noerr(fs.path_for_dir(output_dir, rel_path))

            for name in files:
                in_file_path = fs.join(input_dir, rel_path, name)
                out_file_path = fs.join(output_dir, rel_path, name)

                with open(out_file_path, 'w') as out_file,\
                     open(in_file_path, 'r') as in_file:
                        out_file.write(in_file.read())

        # Copy resources
        self.project.copy_resources(out_format)
