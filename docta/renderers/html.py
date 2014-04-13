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

        # Jinja
        template_loader = jinja2.FileSystemLoader(self.project.templates_dir())
        self.jinja = jinja2.Environment(loader=template_loader)
        self.jinja.globals.update(**self.template_globals())

    def render(self):
        out_format = self.out_format
        output_dir = self.project.output_dir(out_format)

        # Prepare output dir
        fs.mkdirs(output_dir)

        # Render chapters
        home = True
        for chapter in self.project.tree:
            self.render_chapter(chapter, home=home)
            home = False  # only the first root chapter is 'home'

        # Copy resources
        self.project.copy_resources(out_format)

    def render_chapter(self, chapter, home=False):
        # print("Render: %s" % str(chapter))
        output_dir = self.project.output_dir(self.out_format)

        # dir for index
        if chapter.is_index:
            # print(fs.path_for_dir(output_dir, chapter.rel_dir_path))
            fs.mkdirs(fs.path_for_dir(output_dir, chapter.rel_dir_path))

        # load content - render - flush content
        chapter.load_content()

        if not chapter.content is None:
            out_file_path = fs.join(output_dir, chapter.rel_dir_path,
                                    self.get_html_name(chapter))
            # print(out_file_path)

            if home:
                template = self.get_template('home.html')
            elif chapter.is_index:
                template = self.get_template('index.html')
            else:
                template = self.get_template('page.html')

            with open(out_file_path, 'w') as out_file:
                context = self.get_context(chapter)
                html = template.render(**context)
                out_file.write(html)
        
        chapter.flush_content()

        # render children
        for child in chapter.children:
            self.render_chapter(child)

    def get_template(self, path):
        """
        Get Jinja template by path.
        """
        return self.jinja.get_template(path)

    def get_html_name(self, chapter):
        """
        Get .html file name chapter.
        """
        if chapter.is_index:
            bits = (HTML_INDEX[0],)
        else:
            bits = chapter.file_name.rsplit('.', 1)
        return '.'.join((bits[0], HTML_INDEX[1]))

    def get_url(self, chapter):
        """
        Get URL for chapter.
        """
        base_url = chapter.config['server']['base_url'].rstrip('/')
        if chapter.is_index:
            return '/'.join((base_url, chapter.nav_path))
        else:
            return '/'.join((base_url, '%s.%s' % (chapter.nav_path, HTML_INDEX[1])))

    def template_globals(self):
        base_url = self.project.config['server']['base_url'].rstrip('/')
        assets_url = self.project.config['server']['assets_url'].rstrip('/')
        return {
            'url': lambda u: '/'.join((base_url, u)),
            'asset': lambda a: '/'.join((base_url, assets_url, a)),
            'chapter_url': lambda chapter: self.get_url(chapter),
            'markdown': lambda text: md.html(text)
        }

    def get_context(self, chapter):
        """
        Template context for chapter.
        """
        context = {
            'project': {
                'title': self.project.config['title'],
                'logo': self.project.config['logo'],
                'copyright': self.project.config['copyright'],
                'tree': self.project.tree,
            },
            'chapter': chapter,
        }
        return context
