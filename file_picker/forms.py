from django import forms
from django.db.models import Q

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
