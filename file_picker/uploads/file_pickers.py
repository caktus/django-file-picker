from django import forms
from django.core.files.base import ContentFile

import file_picker
from file_picker.uploads.models import File, Image


class ImageForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    class Meta(object):
        model = Image
        fields = ('name', 'description')

    def save(self, commit=True):
        image = super(ImageForm, self).save(commit=False)
        file_path = self.cleaned_data['file']
        fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
        image.file.save(file_path, fh)
        if commit:
            image.save()
        return image


class FileForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    class Meta(object):
        model = File
        fields = ('name', 'description')

    def save(self, commit=True):
        image = super(FileForm, self).save(commit=False)
        file_path = self.cleaned_data['file']
        fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
        image.file.save(file_path, fh)
        if commit:
            image.save()
        return image


class ImagePicker(file_picker.ImagePickerBase):
    form = ImageForm
    columns = ('name', 'file_type', 'date_modified')
    extra_headers = ('Name', 'File Type', 'Date Modified')
    

class FilePicker(file_picker.FilePickerBase):
    form = FileForm
    columns = ('name', 'file_type', 'date_modified')
    extra_headers = ('Name', 'File type', 'Date modified')
    

file_picker.site.register(Image, ImagePicker, name='images')
file_picker.site.register(File, FilePicker, name='files')

