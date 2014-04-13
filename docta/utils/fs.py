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
    if isdir(path):
        shutil.rmtree(path, ignore_errors=ignore_errors)
    else:
        try:
            os.unlink(path)
        except (OSError, IOError) as e:
            if not ignore_errors:
                raise e


def cp(src, dst, overwrite=False, _listcopy=False):
    """Copy files or directories recursively."""
    # top-dir to existing top-dir
    if not _listcopy:
        if isdir(src) and isdir(dst):
            for name in os.listdir(src):
                cp(join(src, name), join(dst, name),
                   overwrite=overwrite, _listcopy=True)
            return
    
    # overwrite
    if overwrite:
        rm(dst, ignore_errors=True)

    # now copy!
    if isdir(src):
        shutil.copytree(src, dst)
    elif isfile(src):
        shutil.copy2(src, dst)


def path_for_file(base, relative):
    """Get real directory path by base dir and relative file path."""
    return real(dirname(join(base, relative)))


def path_for_dir(base, relative):
    """Get real directory path by base dir and relative dir path."""
    return real(join(base, relative))
