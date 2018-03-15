from django import forms
from django.utils.translation import ugettext as _


class ContactForm(forms.Form):
    subject = forms.CharField(
        label=_('subject'),
    )

    phone = forms.CharField(
        required=False,
        label=_('phone'),
    )

    name = forms.CharField(
        label=_('name'),
    )

    email = forms.EmailField(
        label=_('email'),
    )

    message = forms.CharField(
        label=_('message'),
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

        if request.user.is_authenticated:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
