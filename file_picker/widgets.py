from django import forms


class FilePickerWidget(forms.Textarea):
    """ Base file picker widget that can be extended """

    def __init__(self, pickers, *args, **kwargs):
        self.pickers = pickers
        classes = kwargs.pop('classes', ['filepicker'])
        super(FilePickerWidget, self).__init__(*args, **kwargs)
        if 'file' in pickers:
            classes.append("file_picker_name_file_%s" % pickers['file'])
        if 'image' in pickers:
            classes.append("file_picker_name_image_%s" % pickers['image'])
        self.attrs['class'] = ' '.join(classes)


class SimpleFilePickerWidget(FilePickerWidget):
    """ Basic widget that provides Image/File links """

    def __init__(self, pickers, *args, **kwargs):
        kwargs['classes'] = ['simple-filepicker']
        super(SimpleFilePickerWidget, self).__init__(pickers, *args, **kwargs)

    class Media:
        css = {"all": ("css/filepicker.overlay.css",)}
        js = ("js/ajaxupload.js",
              "js/jquery.filepicker.js",
              "js/jquery.filepicker.simple.js")
