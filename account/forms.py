from django import forms
from django.forms import Form
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import PasswordResetForm

from account.models import User
from entrepreneur.models import CompanyScore


class SignUpForm(Form):
    """Sign up form. Basic information to create
    an user session is required here.
    """
    first_name = forms.CharField(
        label=_('First name'),
        required=True,
        max_length=50,
        error_messages={
            'required': _('This field is required.'),
        },
    )

    last_name = forms.CharField(
        label=_('Last name'),
        required=True,
        max_length=50,
        error_messages={
            'required': _('This field is required.'),
        },
    )

    email = forms.EmailField(
        label=_('Email'),
        required=True,
        max_length=50,
        error_messages={
            'required': _('This field is required.'),
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Password"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoginForm(Form):
    """Log in form. User email and password are required here.
    """
    email = forms.EmailField(
        label=_('email'),
        required=True,
        max_length=50,
        error_messages={
            'required': _('This field is required.'),
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=_('password'),
        required=True,
        max_length=50,
        error_messages={
            'required': _('This field is required.'),
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = _('email')
        self.fields['password'].widget.attrs['placeholder'] = _('password')


class ProfileForm(ModelForm):
    """Edit profile form. This form is used to edit
    basic information about users. The 'country_search' field
    and the 'city_search' field are used to search registered
    countries and cities in the application and to autocomplete
    their names.
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'country',
            'state',
            'city',
        ]

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get('country')
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')

        if state.country != country:
            raise forms.ValidationError('Bad data')

        if city.state != state:
            raise forms.ValidationError('bad data')


class ProfileDescriptionForm(Form):
    """This form is used to edit information about
    users professional profile. The profile description
    fields are available in English and Spanish. This
    form is managed by using AJAX requests.
    """
    description_en = forms.CharField(
        required=False,
        min_length=40,
        label=_('description'),
        widget=forms.Textarea,
    )

    description_es = forms.CharField(
        required=False,
        min_length=40,
        label=_('description'),
        widget=forms.Textarea,
    )


class UserPasswordResetForm(PasswordResetForm):
    """Form used to activate the password recovery function.
    It inherits from the basic django form 'PasswordResetForm'.
    This form has only the email field. Registered users must
    enter their email and an mail will be sent with instructions
    to reset their password.
    """
    required_css_class = 'required'

    def get_users(self, email):
        """
        Find accounts with the entered email and send a mail
        with instructions to reset their password.
        """
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        return (u for u in active_users)


class ProfileAutocompleteForm(Form):
    """
    Form used to autocomplete users name by name, username or email.
    """
    userprofile = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Search by name, email or username'),
            },
        ),
        label='',
    )


class UserMessageForm(Form):
    """
    Form to create a private message. Private messages
    can be from users to companies, from users to users or
    from companies to users.
    """
    user_message = forms.CharField(
        label=_('message'),
        widget=forms.Textarea,
    )

    user_to_id = forms.IntegerField(required=False)
    company_to_id = forms.IntegerField(required=False)
    company_from_id = forms.IntegerField(required=False)


class CompanyScoreForm(ModelForm):
    """
    Form to create and update a company score item.
    """
    score = forms.FloatField()

    comment = forms.CharField(
        required=False,
        label=_('country'),
        widget=forms.Textarea,
    )

    class Meta:
        model = CompanyScore
        fields = [
            'score',
            'comment',
        ]


class AvatarForm(Form):
    """
    Form to update profile image. THis form is managed by
    using AJAX requests.
    """
    avatar = forms.ImageField()
