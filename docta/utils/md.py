"""
Provides unified Markdown rendering tools.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import misaka as mi

__all__ = ['markdown']

ALIAS_EXT = {
    'autolink': mi.EXT_AUTOLINK,
    'fenced_code': mi.EXT_FENCED_CODE,
    'lax_html': mi.EXT_LAX_HTML_BLOCKS,
    'lax_html_blocks': mi.EXT_LAX_HTML_BLOCKS,
    'no_intra_emphasis': mi.EXT_NO_INTRA_EMPHASIS,
    'space_headers': mi.EXT_SPACE_HEADERS,
    'strikethrough': mi.EXT_STRIKETHROUGH,
    'superscript': mi.EXT_SUPERSCRIPT,
    'tables': mi.EXT_TABLES,
}

ALIAS_RENDER = {
    'escape': mi.HTML_ESCAPE,
    'hard_wrap': mi.HTML_HARD_WRAP,
    'wrap': mi.HTML_HARD_WRAP,
    'safelink': mi.HTML_SAFELINK,
    'skip_html': mi.HTML_SKIP_HTML,
    'no_html': mi.HTML_SKIP_HTML,
    'skip_images': mi.HTML_SKIP_IMAGES,
    'no_images': mi.HTML_SKIP_IMAGES,
    'skip_links': mi.HTML_SKIP_LINKS,
    'no_links': mi.HTML_SKIP_LINKS,
    'skip_style': mi.HTML_SKIP_STYLE,
    'no_style': mi.HTML_SKIP_STYLE,
    'smartypants': mi.HTML_SMARTYPANTS,
    'toc': mi.HTML_TOC,
    'toc_tree': mi.HTML_TOC_TREE,
    'use_xhtml': mi.HTML_USE_XHTML,
    'xhtml': mi.HTML_USE_XHTML,
}


def get_flags(**options):
    """
    Get flags for provided options to setup Markdown renderer.
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


def markdown(text, **options):
    """
    Parses the provided Markdown-formatted text into valid HTML.
    """
    options.update({
        'no_intra_emphasis': True,
        'autolink': True,
        'wrap': True,
        'tables': True,
        'fenced_code': True,
        'strikethrough': True,
        'smartypants': True,
    })
    ext, rndr = get_flags(**options)
    return mi.html(text, extensions=ext, render_flags=rndr)
