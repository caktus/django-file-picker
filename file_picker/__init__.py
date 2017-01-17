from file_picker.views import FilePickerBase, ImagePickerBase
from file_picker.sites import site, FilePickerSite
from file_picker import widgets

VERSION = (0, 6, 0,)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'file_picker.apps.FilePickerConfig'
