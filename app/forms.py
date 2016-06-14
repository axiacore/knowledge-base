from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(label='Search', max_length=100)
