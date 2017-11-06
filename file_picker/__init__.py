# Aliases allow users to import directly from file_picker.*
from file_picker.views import FilePickerBase, ImagePickerBase  # noqa
from file_picker.sites import site, FilePickerSite  # noqa
from file_picker import widgets  # noqa

VERSION = (0, 9, 1,)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'file_picker.apps.FilePickerConfig'
