"""
Provides HTML rendered.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
import jinja2
import docta.renderers.base as base
import docta.utils.fs as fs
import docta.utils.md as md
import docta.utils.meta as meta

HTML_INDEX = ('index', 'html')


class Renderer(base.BaseRenderer):
    """
    Renders project to HTML files mirroring source dirs structure.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_name = fs.basename(self.project.index_file())

        # Jinja
        template_loader = jinja2.FileSystemLoader(self.project.templates_dir())
        self.jinja = jinja2.Environment(loader=template_loader)
        self.jinja.globals.update(**self.get_extra_globals())

    def render(self):
        out_format = self.out_format
        input_dir = self.project.input_dir()
        output_dir = self.project.output_dir(out_format)
        input_tree = self.project.input_tree

        # Prepare output dir
        fs.mkdirs(output_dir)

        # Templates
        template_index = self.get_template('index.html')
        template_page = self.get_template('page.html')

        # Render output files
        for rel_path, files, files_meta in input_tree:
            fs.mkdirs(fs.path_for_dir(output_dir, rel_path))

            for name in files:
                if not rel_path and name == self.index_name:
                    template = template_index
                else:
                    template = template_page

                in_file_path = fs.join(input_dir, rel_path, name)
                out_file_path = fs.join(output_dir, rel_path, self.get_html_name(name))

                with open(out_file_path, 'w') as out_file,\
                     open(in_file_path, 'r') as in_file:
                        raw_content = md.markdown(meta.stripped(in_file))
                        page_meta = files_meta.get(name, {})
                        page_html = self.render_template(template, raw_content, **page_meta)
                        out_file.write(page_html)

        # Copy resources
        self.project.copy_resources(out_format)

    def get_template(self, path):
        """
        Get Jinja template by path.
        """
        return self.jinja.get_template(path)

    def get_html_name(self, name):
        """
        Get .html file name for any other source file name.
        """
        if name == self.index_name:
            bits = (HTML_INDEX[0],)
        else:
            bits = name.rsplit('.', 1)
        return '.'.join((bits[0], HTML_INDEX[1]))

    def get_extra_globals(self):
        base_url = self.project.config['server']['base_url'].rstrip('/')
        assets_url = self.project.config['server']['assets_url'].rstrip('/')
        return {
            'url': lambda u: '/'.join((base_url, u)),
            'asset': lambda a: '/'.join((base_url, assets_url, a)),
        }

    def render_template(self, template, raw_content, **page_meta):
        """
        Render specified template with project and page data.
        """
        context = {
            'project': self.project,
            'page': {
                'html': raw_content,
            }
        }
        context['page'].update(page_meta)
        return template.render(**context)
