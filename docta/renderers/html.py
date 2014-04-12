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
        output_dir = self.project.output_dir(out_format)

        # Prepare output dir
        fs.mkdirs(output_dir)

        # Render chapters
        for chapter in self.project.tree:
            self.render_chapter(chapter, {
                    'index': self.get_template('index.html'),
                    'page': self.get_template('page.html')})

        # Copy resources
        self.project.copy_resources(out_format)

    def render_chapter(self, chapter, templates):
        # print("Render: %s" % str(chapter))
        output_dir = self.project.output_dir(self.out_format)
        input_dir = self.project.input_dir()
        in_file_path = chapter.file_path

        # dir for index
        if chapter.dir_path:
            # print(fs.path_for_dir(output_dir, chapter.dir_path))
            fs.mkdirs(fs.path_for_dir(output_dir, chapter.dir_path))

        # render file
        if in_file_path:
            file_dir = fs.dirname(in_file_path)
            rel_path = file_dir.replace(input_dir, '').strip(fs.sep)
            out_file_path = fs.join(output_dir, rel_path, self.get_html_name(chapter.file_name))

            if not chapter.parent:
                template = templates['index']
            else:
                template = templates['page']

            with open(out_file_path, 'w') as out_file,\
                 open(in_file_path, 'r') as in_file:
                    raw_content = md.html(meta.stripped(in_file))
                    page_html = self.render_template(template, raw_content, chapter)
                    out_file.write(page_html)

            # print(out_file_path)

        for child in chapter.children:
            self.render_chapter(child, templates)

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

    def render_template(self, template, raw_content, chapter):
        """
        Render specified template with project and page data.
        """
        context = {
            'project': {
                'title': self.project.config['title'],
                'logo': self.project.config['logo'],
                'copyright': self.project.config['copyright'],
                'tree': self.project.tree,
            },
            'page': {
                'html': raw_content,
            },
            'chapter': chapter,
        }
        return template.render(**context)
