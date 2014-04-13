"""
Shortcuts for file system operations.
"""
import os
import os.path
import shutil
import docta.exceptions

dirname = os.path.dirname
basename = os.path.basename
join = os.path.join
real = os.path.realpath
sep = os.path.sep
isfile = os.path.isfile
isdir = os.path.isdir


@docta.exceptions.suppress(OSError, IOError)
def mkdirs(path):
    """Creates dirs recursivelly with permissions mask 0755 +
    ignores OSError and IOError errors."""
    return os.makedirs(path, mode=0755)


def rm(path, ignore_errors=False):
    """Remove files and directories recursivelly."""
    if isdir(path):
        shutil.rmtree(path, ignore_errors=ignore_errors)
    elif isfile(path):
        try:
            os.unlink(path)
        except (OSError, IOError) as e:
            if not ignore_errors:
                raise e


def cp(src, dst, overwrite=False):
    """Copy files and directories recursively."""
    # overwrite file-to-any and dir-to-file
    if overwrite and (isfile(src) or (isdir(src) and isfile(dst))):
        rm(dst, ignore_errors=True)

    # file-to-...
    if isfile(src):
        dst_dir = dirname(dst)
        if not isdir(dst_dir):
            mkdirs(dst_dir)
        shutil.copy2(src, dst)
    # dir-to-...
    elif isdir(src):
        for name in os.listdir(src):
            cp(join(src, name), join(dst, name), overwrite=overwrite)


def path_for_file(base, relative):
    """Get real directory path by base dir and relative file path."""
    return real(dirname(join(base, relative)))


def path_for_dir(base, relative):
    """Get real directory path by base dir and relative dir path."""
    return real(join(base, relative))
