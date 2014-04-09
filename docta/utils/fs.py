"""
Shortcuts for file system operations.
"""
import os.path
import docta.exceptions

dirname = os.path.dirname
filename = os.path.basename
join = os.path.join
real = os.path.realpath
sep = os.path.sep


@docta.exceptions.suppress(OSError, IOError)
def mkdirs(path):
    """Creates dirs recursivelly with permissions mask 0755 +
    ignores OSError and IOError errors."""
    return os.makedirs(path, mode=0755)


def path_for_file(base, relative):
    """Get real directory path by base dir and relative file path."""
    return real(dirname(join(base, relative)))


def path_for_dir(base, relative):
    """Get real directory path by base dir and relative dir path."""
    return real(join(base, relative))
