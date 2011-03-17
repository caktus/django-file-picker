import os

from django import forms
from django.db import models
from django.db.models import Q, get_model
from django.db.models.base import FieldDoesNotExist

from django.core.files.base import ContentFile


class QueryForm(forms.Form):
    page = forms.IntegerField(min_value=0, required=False)
    search = forms.CharField(
        max_length=300, required=False,
    )
    
    def clean_page(self):
        page = self.cleaned_data.get('page')
        if not page:
            page = 1
        return page


FIELD_EXCLUDES = (models.ImageField, models.FileField)


def model_to_AjaxItemForm(model):
    exclude = []
    for field_name in model._meta.get_all_field_names():
        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            exclude.append(field_name)
            continue
        if isinstance(field, FIELD_EXCLUDES):
            exclude.append(field_name)
    meta = type('Meta', (), { "model":model, "exclude": exclude})
    modelform_class = type('modelform', (AjaxItemForm,), {"Meta": meta})
    return modelform_class


class AjaxItemForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if not os.path.exists(file):
            raise forms.ValidationError('Missing file')
        return file
        
    def save(self, *args, **kwargs):
        item = super(AjaxItemForm, self).save(commit=False)
        getattr(item, self.Meta.exclude[0]).save(self.cleaned_data['file'],
            ContentFile(open(str(self.cleaned_data['file']),'r').read())
        )
        item.save(*args, **kwargs)
        return item
