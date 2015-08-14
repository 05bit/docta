# -*- coding: utf-8 -*-
"""
Provides Markdown rendering utils on top of Mistune.
"""
from __future__ import absolute_import, unicode_literals
from mistune import escape, Markdown, Renderer, InlineLexer
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

__all__ = ('html',)


class HighlightRenderer(Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


def html(text):
    return markdown(text)


renderer = HighlightRenderer(hard_wrap=True)
markdown = Markdown(renderer)
