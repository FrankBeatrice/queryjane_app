from django import forms
from django.utils.translation import ugettext as _

from .models import LegalItem


class LegalItemForm(forms.ModelForm):
    """
    Legal item update form. Only platform administrator
    users can submit this form. The 'notify_users' field
    must be checked only if the change is about terms.
    """
    notify_users = forms.BooleanField(
        required=False,
        label=_('notify users'),
        help_text=_('Check it to notify users about important changes.'),
    )

    class Meta:
        model = LegalItem
        fields = [
            'sp_description',
            'en_description',
        ]


class ContactForm(forms.Form):
    """
    Contact form. If user is authenticated, the
    name and email fields are filled previously
    and can not be edited.
    """
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
