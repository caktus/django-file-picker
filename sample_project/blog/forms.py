from django import forms
from django.db.models import get_model
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
        
class InlinePageletForm(forms.ModelForm):
    content = forms.CharField(widget=WYMEditor())
    class Meta:
        model = pagelets.InlinePagelet
