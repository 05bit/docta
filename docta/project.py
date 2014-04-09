"""
Docta projects handler.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *


class DoctaProject(object):
    """
    Project data handler: scans project directories, manages resources,
    creates output directories, creates empty project, builds project.
    """
    def __init__(self, path, **config):
        self.path = path
        self.config = config

    def load(self):
        """
        Load project structure and files.
        """
        raise Exception(NotImplemented)

    def build(self, formats=None):
        """
        Build project with specified formats.
        """
        raise Exception(NotImplemented)

    def init(self):
        """
        Init empty project.
        """
        raise Exception(NotImplemented)

    def create_output_dir(self, format=None):
        """
        Create output directory if doesn't exist.
        """
        raise Exception(NotImplemented)

    def copy_resources(self, format=None):
        """
        Copy resources to output directory.
        """
        raise Exception(NotImplemented)
