from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class SearchForm(forms.Form):
    text = forms.CharField(label='Search', max_length=100)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_('This email is not registered'))

        return email.strip().lower()
