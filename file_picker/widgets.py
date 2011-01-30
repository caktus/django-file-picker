from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


class FilePickerWidget(forms.Textarea):
    def __init__(self, pickers, *args, **kwargs):
        self.pickers = pickers
        classes = kwargs.pop('classes', ['filepicker'])
        super(FilePickerWidget, self).__init__(*args, **kwargs)
        if 'file' in pickers:
            classes.append("file_picker_name_file_%s" % pickers['file'])
        if 'image' in pickers:
            classes.append("file_picker_name_image_%s" % pickers['image'])
        self.attrs['class'] = ' '.join(classes)


class WYMeditorWidget(FilePickerWidget):
    def __init__(self, pickers, *args, **kwargs):
        kwargs['classes'] = ['wymeditor']
        super(WYMeditorWidget, self).__init__(pickers, *args, **kwargs)

