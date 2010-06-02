from django import forms
from django.db.models import get_model
from sample_project.article.widgets import FilePickerForm

from django.core.files.base import ContentFile

class ImageForm(forms.Form):
    pass
    
class PostAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=FilePickerForm())
    class Meta:
        model = get_model('article', 'post')
        

class AjaxImageForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())    
        
    class Meta:
        model = get_model('article', 'image')
        exclude = ['file']
        
    def save(self, *args, **kwargs):
        item = super(AjaxImageForm, self).save(commit=False)
        item.file.save(self.cleaned_data['file'],
            ContentFile(open(str(self.cleaned_data['file']),'r').read())
        )
        item.save(*args, **kwargs)
