from django import forms
from django.db.models import get_model
from sample_project.article.widgets import FilePickerForm

class ImageForm(forms.Form):
    pass
    
class PostAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=FilePickerForm())
    class Meta:
        model = get_model('article', 'post')
