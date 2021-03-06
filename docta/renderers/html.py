"""
Provides HTML rendered.
"""
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import super
from functools import partial
import jinja2
import random
import docta.renderers.base as base
import docta.utils.fs as fs
import docta.utils.md2 as md
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

        # Copy assets
        self.project.copy_assets(out_format)

        # Copy resources
        self.project.copy_resources(out_format)

    def render_chapter(self, chapter, home=False):
        # print("Render: %s" % str(chapter))
        output_dir = self.project.output_dir(self.out_format)

        # dir for index
        # if chapter.is_index:
        #     # print(fs.path_for_dir(output_dir, chapter.rel_dir_path))
        #     fs.mkdirs(fs.path_for_dir(output_dir, chapter.rel_dir_path))

        # load content - render - flush content
        chapter.load_content()

        if not chapter.content_raw is None:
            out_file_path = fs.join(output_dir, chapter.rel_dir_path,
                                    self.get_html_name(chapter))
            fs.mkdirs(fs.dirname(out_file_path))
            # print(out_file_path)

            if 'template' in chapter.meta:
                template = self.get_template(chapter.meta['template'])
            elif home:
                template = self.get_template('home.html')
            elif chapter.is_index:
                template = self.get_template('index.html')
            else:
                template = self.get_template('page.html')

            with fs.open(out_file_path, 'w') as out_file:
                context = self.template_context(chapter)
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
        Get .html file name for chapter.
        """
        if chapter.is_index:
            return 'index.html'
        else:
            parts = chapter.file_name.rsplit('.', 1)
            return fs.sep.join((parts[0], 'index.html'))
        # if chapter.is_index:
        #     bits = (HTML_INDEX[0],)
        # else:
        #     bits = chapter.file_name.rsplit('.', 1)
        # return '.'.join((bits[0], HTML_INDEX[1]))

    def get_chapter_url(self, chapter):
        """
        Get URL for chapter.
        """
        base_url = chapter.config['server']['base_url']
        if chapter.nav_path:
            return '/'.join((base_url.rstrip('/'), chapter.nav_path, ''))
        else:
            return base_url

    def main_menu_config(self):
        """
        Main menu config.
        """
        config = self.project.config['output'][self.out_format]
        return config.get('main_menu', [])

    def theme_config(self):
        """
        Theme config.
        """
        config = self.project.config['output'][self.out_format]
        return config.get('theme', {})

    def template_globals(self):
        base_url = self.project.config['server']['base_url'].rstrip('/')
        assets_url = self.project.config['server']['assets_url'].strip('/')
        icon_template = self.get_template('icon.html')
        icon_context = {'theme': self.theme_config()}
        return {
            'asset': partial(get_asset_url, project=self.project),
            'chapter_url': self.get_chapter_url,
            'markdown': md.html,
            'url': partial(url_full, base_url=base_url),
            'url_external': url_is_external,
            'icon': lambda i: icon_template.render(icon=i, **icon_context) if i else '',
            'safe': lambda s: jinja2.Markup(s),
            'random': random.random,
        }

    def template_context(self, chapter):
        """
        Template context for chapter.
        """
        context = {
            'project': {
                'title': self.project.config.get('title'),
                'logo': self.project.config.get('logo'),
                'copyright': self.project.config.get('copyright'),
                'extras': self.project.config.get('extras'),
                'main_menu': self.main_menu_config(),
                'tree': self.project.tree,
            },
            'chapter': chapter,
            'theme': self.theme_config(),
        }
        return context


##
## Template helper functions
##


def get_asset_url(rel_path, project, use_hash=False):
    base_url = project.config['server']['base_url'].rstrip('/')
    assets_url = project.config['server']['assets_url'].strip('/')
    full_url = '/'.join((base_url, assets_url, rel_path))
    if use_hash:
        hash_str = project.asset_hash(rel_path)
        full_url += '?_=%s' % hash_str
    return full_url


def url_is_external(u):
    return '://' in u


def url_is_absolute(u):
    return u.startswith('/')


def url_is_anchor(u):
    return u.startswith('#')


def url_full(u, base_url=''):
    if url_is_external(u) or url_is_absolute(u) or url_is_anchor(u):
        return u
    return '/'.join((base_url, u))
