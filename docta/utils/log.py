"""
Logging and print helpers.
"""
from __future__ import absolute_import, print_function, unicode_literals
import os
import sys
import docta.utils.fs as fs

ERROR_LOGFILE = 'docta-error.log'

MARK_BLUE = '\033[34m'  # info
MARK_GREEN = '\033[32m'  # success
MARK_YELL = '\033[33m'  # warning
MARK_RED = '\033[31m'  # error
MARK_PURPLE = '\033[35m'
MARK_BLACK = '\033[30m'
MARK_WHITE = '\033[37m'
MARK_BOLD = '\033[1m'
MARK_END = '\033[0m'  # closing symbol

def exc_to_str(e):
    """
    Exception as string.
    """
    return getattr(e, 'message', None) or str(e)


def error(message, out=None):
    """
    Write message to `sys.stderr`.
    """
    pre, post = '', ''
    if out is None:
        out = sys.stderr
        pre, post = MARK_RED, MARK_END
    out.write(pre + ('fatal: %s' % message) + post + '\n')


def message(message, out=None):
    """
    Write message to `sys.stderr`.
    """
    pre, post = '', ''
    if out is None:
        out = sys.stdout
        # pre, post = MARK_BLUE, MARK_END
    out.write(pre + ('%s' % message) + post + '\n')


def success(message, out=None):
    """
    Write message to `sys.stderr`.
    """
    pre, post = '', ''
    if out is None:
        out = sys.stdout
        pre, post = MARK_GREEN, MARK_END
    out.write(pre + ('%s' % message) + post + '\n')


def traceback(out=None):
    """
    Dump traceback to error log file.
    """
    import traceback as tb

    need_close = False
    if out is None:
        out = fs.open(ERROR_LOGFILE, 'w')
        need_close = True

    out.write('-' * 60 + '\n')
    tb.print_exc(limit=20, file=out)
    out.write('-' * 60 + '\n')

    if need_close:
        out.close()


def cleanup():
    """
    Cleanup error log.
    """
    if fs.isfile(ERROR_LOGFILE):
        os.unlink(ERROR_LOGFILE)
