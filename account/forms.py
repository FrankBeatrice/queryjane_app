from django import forms
from django.forms import Form
from django.contrib.auth.forms import PasswordResetForm

from account.models import User


class SignUpForm(Form):
    """Formulario de creación de usuarios
    """
    first_name = forms.CharField(
        label='nombre',
        required=True,
        max_length=50,
        error_messages={
            'required': 'Este campo es requerido.',
        },
    )

    last_name = forms.CharField(
        label='apellidos',
        required=True,
        max_length=50,
        error_messages={
            'required': 'Este campo es requerido.',
        },
    )

    email = forms.EmailField(
        label=u'correo electrónico',
        required=True,
        max_length=50,
        error_messages={
            'required': 'Este campo es requerido.',
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=u"contraseña",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoginForm(Form):
    email = forms.EmailField(
        label=u'correo electrónico',
        required=True,
        max_length=50,
        error_messages={
            'required': u'Este campo es requerido.',
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=u'Contraseña',
        required=True,
        max_length=50,
        error_messages={
            'required': 'Este campo es requerido.',
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = 'Correo electrónico'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


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
                'placeholder': 'Busca por nombre o correo electrónico',
            },
        ),
        label='',
    )
