from django import forms


class QueryForm(forms.Form):
    page = forms.IntegerField(min_value=0, required=False)

    def clean_page(self):
        page = self.cleaned_data.get('page')
        if not page:
            page = 0
        return page
