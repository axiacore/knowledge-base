from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.forms import Textarea


class SearchForm(forms.Form):
    q = forms.CharField(label=_('Search'), max_length=100)


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Email'), max_length=150)

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()

        user, domain = email.split('@')
        if domain not in settings.ALLOWED_DOMAINS:
            raise ValidationError(_('This email is not allowed to login'))
        elif not User.objects.filter(username=email).exists():
            User.objects.create_user(username=email)

        return email


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        label=_('Your email'),
        max_length=150
    )

    description = forms.CharField(
        label=_('Tell us why it wasn\'t helpful'),
        max_length=500,
        widget=forms.Textarea(
            attrs={'rows': 5}
        )
    )
