"""
Provides base class `BaseRenderer` for sublassing by specific renderers.
"""


class BaseRenderer(object):
    """
    Base renderer class.

    Constructor:

        BaseRenderer(project)

    Methods to implement:

        BaseRenderer.render(only=None)
    """
    out_format = None

    def __init__(self, project):
        self.project = project

    def render(self):
        """
        Implement `render()` in subclass.
        """
        raise Exception(NotImplemented)
