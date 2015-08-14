"""
Provides Markdown rendering utils on top of Misaka.
"""
from __future__ import absolute_import, print_function, unicode_literals
import misaka as m
import pygments
import pygments.lexers as lexers
import pygments.formatters

# Python 3.x
try:
    from html import escape as escape_html
# Python 2.x
except ImportError:
    from cgi import escape as escape_html

__all__ = ['markdown']

ALIAS_EXT = {
    'autolink': m.EXT_AUTOLINK,
    'fenced_code': m.EXT_FENCED_CODE,
    'lax_html': m.EXT_LAX_HTML_BLOCKS,
    'lax_html_blocks': m.EXT_LAX_HTML_BLOCKS,
    'no_intra_emphasis': m.EXT_NO_INTRA_EMPHASIS,
    'space_headers': m.EXT_SPACE_HEADERS,
    'strikethrough': m.EXT_STRIKETHROUGH,
    'superscript': m.EXT_SUPERSCRIPT,
    'tables': m.EXT_TABLES,
}

ALIAS_RENDER = {
    'escape': m.HTML_ESCAPE,
    'hard_wrap': m.HTML_HARD_WRAP,
    'wrap': m.HTML_HARD_WRAP,
    'safelink': m.HTML_SAFELINK,
    'skip_html': m.HTML_SKIP_HTML,
    'no_html': m.HTML_SKIP_HTML,
    'skip_images': m.HTML_SKIP_IMAGES,
    'no_images': m.HTML_SKIP_IMAGES,
    'skip_links': m.HTML_SKIP_LINKS,
    'no_links': m.HTML_SKIP_LINKS,
    'skip_style': m.HTML_SKIP_STYLE,
    'no_style': m.HTML_SKIP_STYLE,
    'smartypants': m.HTML_SMARTYPANTS,
    'toc': m.HTML_TOC,
    'toc_tree': m.HTML_TOC_TREE,
    'use_xhtml': m.HTML_USE_XHTML,
    'xhtml': m.HTML_USE_XHTML,
}


def get_flags(**options):
    """
    Get flags for Markdown renderer by options dict.
    """
    ext = 0
    for name, val in ALIAS_EXT.items():
        if options.get(name):
            ext = ext | val
        if name.startswith("no_"):
            if options.get(name[3:]) is False:
                ext = ext | val

    rndr = 0
    for name, val in ALIAS_RENDER.items():
        if options.get(name):
            rndr = rndr | val
        if name.startswith("no_"):
            if options.get(name[3:]) is False:
                rndr = rndr | val

    return ext, rndr


class Renderer(m.HtmlRenderer, m.SmartyPants):
    """
    HTML renderer with Pygments highlight support.
    """
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                escape_html(text.strip())
        lexer = lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.HtmlFormatter(cssclass='source')
        return pygments.highlight(text, lexer, formatter)


def html(text, **options):
    """
    Renders Markdown text to valid HTML.
    """
    # Prepare
    options.update({
        'no_intra_emphasis': True,
        'autolink': True,
        'wrap': True,
        'tables': True,
        'fenced_code': True,
        'strikethrough': True,
        'smartypants': True,
    })
    extensions, render_flags = get_flags(**options)

    # Render!
    renderer = m.Markdown(Renderer(render_flags), extensions=extensions)
    return renderer.render(text)
