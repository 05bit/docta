"""
Chapters handling. Every document page or directory is represented by Chapter.
"""
from __future__ import absolute_import, print_function, unicode_literals
import os
import docta.utils.fs as fs
import docta.utils.meta as meta

# Defaults
INDEX_FILE = 'index.md'


class Chapter(object):
    """
    Chapter is a data container for documents (pages), chapter are
    organized hierarchically.
    """
    def __init__(self, config, title, nav_path, is_index=False):
        # config
        self.config = config
        self.file_path = None
        # data
        self.content = None
        self.title = title
        self.meta = {}
        # structure
        self.parent = None
        self.children = []
        # navigation
        self.nav_path = nav_path
        self.is_index = is_index
        self.rel_dir_path = nav_path.replace('/', fs.sep) if is_index else None

    def __str__(self):
        return '%s (%s)' % (self.title, self.nav_path)

    def __eq__(self, other):
        if other:
            return self.nav_path == other.nav_path
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def load_meta(self, file_path):
        """
        Load meta from file.
        """
        with open(file_path, 'r') as in_file:
            self.meta = meta.extract(in_file)

        self.file_path = file_path
        self.file_name = fs.basename(file_path)
        self.title = self.meta.get('title', self.title)
        self.sorting = self.meta.get('sorting', self.title)

    def load_content(self):
        """
        Load content. Meta have to be loaded before loading content!
        """
        if self.file_path:
            with open(self.file_path, 'r') as in_file:
                self.content = meta.stripped(in_file)

    def flush_content(self):
        """
        Flush chapter content. We're going to do load-render-flush on every
        chaper render so we won't store whole chapters data in memory.
        """
        self.content = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        if not child.is_index:
            child.rel_dir_path = self.rel_dir_path

    @classmethod
    def load_tree(cls, path, config, nav_path=''):
        """
        Load chapters tree recursivelly.
        """
        # print ("Load tree: %s, %s" % (path, config))
        
        # scan sub-dirs and files
        files, dirs = [], []
        for name in os.listdir(path):
            full_path = fs.join(path, name)
            # dirs
            if fs.isdir(full_path):
                if not cls.is_name_masked(name):
                    dirs.append(full_path)
            # files
            elif fs.isfile(full_path):
                if cls.is_file_to_render(name):
                    files.append(name)

        # empty chapter
        if not files and not dirs:
            return

        # no index = no data
        index_name = config.get('index', INDEX_FILE)
        if not index_name in files:
            return

        # create index chapter
        index_title = fs.basename(path).capitalize()
        chapter = cls(config, title=index_title,
                      nav_path=nav_path, is_index=True)
        chapter.load_meta(file_path=fs.join(path, index_name))
        files.remove(index_name)

        # create children
        for name in files:
            file_path = fs.join(path, name)
            file_slug = cls.slug_by_name(name)
            file_nav_path = nav_path and '/'.join((nav_path, file_slug)) or file_slug
            child = cls(config, title=file_slug.capitalize(),
                        nav_path=file_nav_path, is_index=False)
            child.load_meta(file_path)
            chapter.add_child(child)

        for dir_path in dirs:
            dir_slug = fs.basename(dir_path)
            dir_nav_path = nav_path and '/'.join((nav_path, dir_slug)) or dir_slug
            child = cls.load_tree(dir_path, config, nav_path=dir_nav_path)
            if child:
                chapter.add_child(child)

        # print ("chapter: %s, files: %s, dirs: %s" % (str(chapter), files, dirs))
        return chapter

    @classmethod
    def slug_by_name(cls, name):
        return name.rsplit('.', 1)[0]

    @classmethod
    def is_relpath_masked(self, relative):
        """
        Checks if relative dir path is masked (not rendered) in build.
        """
        for name in relative.strip(fs.sep).split(fs.sep):
            if self.is_name_masked(name):
                return True
        return False

    @classmethod
    def is_name_masked(self, name):
        """
        Checks if file/dir name is masked.
        """
        return name.startswith('_') or name.startswith('.')

    @classmethod
    def is_file_to_render(self, name):
        """
        Checks if file is to render.
        """
        if not self.is_name_masked(name):
            if name.endswith('.md'):
                return True
        return False
