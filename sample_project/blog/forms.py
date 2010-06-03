import os

from django import forms
from django.db.models import get_model
from django.core.files.base import ContentFile

from sample_project.blog.widgets import WYMEditor

from pagelets import models as pagelets
from pagelets import forms as pagelets_form

class ImageForm(forms.Form):
    pass
    

class PostAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=WYMEditor())
 
    class Meta:
        model = get_model('blog', 'post')
        

class PageletForm(forms.ModelForm):
    content = forms.CharField(widget=WYMEditor())
    class Meta:
        model = pagelets.Pagelet
    
    def __init__(self, *args, **kwargs):
        super(PageletForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'pagelet-change'})
        
        

class InlinePageletForm(forms.ModelForm):
    content = forms.CharField(widget=WYMEditor())
    class Meta:
        model = pagelets.InlinePagelet

    def __init__(self, *args, **kwargs):
        super(InlinePageletForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'pagelet-change'})
        

class AjaxImageForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    def clean_file(self):
        file = self.cleaned_data['file']
        if not os.path.exists(file):
            raise forms.ValidationErorr('Missing file')
        return file
        
    class Meta:
        model = get_model('blog', 'image')
        exclude = ['file']
        
    def save(self, *args, **kwargs):
        item = super(AjaxImageForm, self).save(commit=False)
        item.file.save(self.cleaned_data['file'],
            ContentFile(open(str(self.cleaned_data['file']),'r').read())
        )
        item.save(*args, **kwargs)
        return item
