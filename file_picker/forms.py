from django import forms
from django.db.models import Q

class QueryForm(forms.Form):
    page = forms.IntegerField(min_value=0, required=False)
    search = forms.CharField(
        min_length=3,max_length=300, required=False,
    )
    
    def clean_page(self):
        page = self.cleaned_data.get('page')
        if not page:
            page = 0
        return page
