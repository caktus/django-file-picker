from file_picker.widgets import FilePickerWidget


class WYMeditorWidget(FilePickerWidget):
    def __init__(self, pickers, *args, **kwargs):
        kwargs['classes'] = ['wymeditor']
        super(WYMeditorWidget, self).__init__(pickers, *args, **kwargs)

    class Media:
        css = {"all": ("css/filepicker.overlay.css",)}
        js = ("js/ajaxupload.js",
              "js/jquery.filepicker.js",
              "wymeditor/jquery.wymeditor.js",
              "js/jquery.wymeditor.filepicker.js")
