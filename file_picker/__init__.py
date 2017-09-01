# Aliases allow users to import directly from file_picker.*
try:
    from file_picker.views import FilePickerBase, ImagePickerBase  # noqa
    from file_picker.sites import site, FilePickerSite  # noqa
    from file_picker import widgets  # noqa
except ImportError:
    # setup.py can't access __version__ unless django and deps are installed
    # We'll deprecate these aliases now, and they should be removed in the next version.
    pass

VERSION = (0, 6, 0,)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'file_picker.apps.FilePickerConfig'
