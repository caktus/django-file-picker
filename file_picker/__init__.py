# Aliases allow users to import directly from file_picker.*
# FIXME: Should we deprecate this behavior? setup.py can't access __version__ unless django and deps are installed
from file_picker.views import FilePickerBase, ImagePickerBase  # noqa
from file_picker.sites import site, FilePickerSite  # noqa
from file_picker import widgets  # noqa

VERSION = (0, 6, 0,)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'file_picker.apps.FilePickerConfig'
