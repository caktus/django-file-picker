VERSION = (0, 5, 0,)
__version__ = '.'.join(map(str, VERSION))

from file_picker.views import FilePickerBase, ImagePickerBase
from file_picker.sites import site, FilePickerSite
from file_picker import widgets


def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            import_module('%s.file_pickers' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'file_pickers'):
                raise
