from django import forms
from django.forms import Form
from django.contrib.auth.forms import PasswordResetForm

from account.models import User


class SignUpForm(Form):
    """Formulario de creación de usuarios
    """
    first_name = forms.CharField(
        label='first name',
        required=True,
        max_length=50,
        error_messages={
            'required': 'This field is required.',
        },
    )

    last_name = forms.CharField(
        label='last name',
        required=True,
        max_length=50,
        error_messages={
            'required': 'This field is required.',
        },
    )

    email = forms.EmailField(
        label=u'email',
        required=True,
        max_length=50,
        error_messages={
            'required': 'This field is required.',
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=u"password",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoginForm(Form):
    email = forms.EmailField(
        label=u'email',
        required=True,
        max_length=50,
        error_messages={
            'required': 'This field is required.',
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=u'password',
        required=True,
        max_length=50,
        error_messages={
            'required': 'This field is required.',
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['password'].widget.attrs['placeholder'] = 'password'


class UserPasswordResetForm(PasswordResetForm):
    required_css_class = 'required'

    def get_users(self, email):
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        return (u for u in active_users)


class ProfileAutocompleteForm(Form):
    userprofile = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by name, email or username',
            },
        ),
        label='',
    )
