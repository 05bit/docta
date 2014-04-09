"""
Shortcuts for file system operations.
"""
import os.path
import docta.exceptions

dirname = os.path.dirname
join = os.path.join
real = os.path.realpath
sep = os.path.sep


def mkdirs(path):
    """Creates dirs recursivelly with permissions mask 0755."""
    return os.makedirs(path, mode=0755)


@docta.exceptions.suppress(OSError, IOError)
def mkdirs_noerr(path):
    """Creates dirs recursivelly with permissions mask 0755 + ignores errors."""
    return mkdirs(path)


def path_for_file(base, relative):
    """Get real directory path by base dir and relative file path."""
    return real(dirname(join(base, relative)))


def path_for_dir(base, relative):
    """Get real directory path by base dir and relative dir path."""
    return real(join(base, relative))
