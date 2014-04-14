"""
Logging and print helpers.
"""
from __future__ import absolute_import, print_function, unicode_literals
import os
import sys
import docta.utils.fs as fs

ERROR_LOGFILE = 'docta-error.log'


def exc_to_str(e):
    """
    Exception as string.
    """
    return getattr(e, 'message', str(e))


def error(message, out=None):
    """
    Write message to `sys.stderr`.
    """
    if out is None:
        out = sys.stderr
    out.write('fatal: %s\n' % message)


def message(message, out=None):
    """
    Write message to `sys.stderr`.
    """
    if out is None:
        out = sys.stdout
    out.write('%s\n' % message)


def traceback(out=None):
    """
    Dump traceback to error log file.
    """
    import traceback as tb

    need_close = False
    if out is None:
        out = open(ERROR_LOGFILE, 'w')
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
