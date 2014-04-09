"""
Rendering tools for Docta.
"""
import importlib


def get_renderer(out_format, **custom):
    """
    Get renderer class for specified format.
    """
    module_name = custom.get(out_format, 'docta.renderers.%s' % out_format)
    render_module = importlib.import_module(module_name)
    render_class = render_module.Renderer
    render_class.out_format = out_format
    return render_class
