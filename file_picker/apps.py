from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class FilePickerConfig(AppConfig):
    name = 'file_picker'

    def ready(self):
        """
        Autodiscover file_pickers modules in other apps.
        """
        autodiscover_modules('file_pickers')
