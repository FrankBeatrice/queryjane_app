from django import forms
from django.forms import Form
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from .data import ACTIVE_MEMBERSHIP
from .data import ADMINISTRATOR_ROLES
from .data import JOB_TYPE_CHOICES
from .models import JobOffer
from .models import Venture
from account.models import IndustryCategory
from account.models import ProfessionalProfile
from entrepreneur.models import AdministratorMembership


class CompanyFilter(forms.Form):
    country_search = forms.CharField(
        required=False,
        label=_('Country'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type the country name and select one from the list.'),
            },
        ),
    )

    country_code = forms.CharField(
        required=False,
        label=_('country code'),
    )

    city_search = forms.CharField(
        required=False,
        label=_('City'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type the city name.'),
            },
        ),
    )

    city_id = forms.CharField(
        required=False,
        label=_('city id'),
    )

    category = forms.ModelChoiceField(
        required=False,
        queryset=IndustryCategory.objects.all(),
        label='Sector',
        empty_label=_('all sectors'),
    )

    company_search = forms.CharField(
        label=_('Search company'),
        required=False,
    )

    company_id = forms.CharField(
        required=False,
        label=_('company id'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class JobOffersFilter(forms.Form):
    country_search = forms.CharField(
        required=False,
        label=_('Country'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type the country name and select one from the list.'),
            },
        ),
    )

    country_code = forms.CharField(
        required=False,
        label=_('country code'),
    )

    city_search = forms.CharField(
        required=False,
        label='City',
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type the city name.'),
            },
        ),
    )

    city_id = forms.CharField(
        required=False,
        label=_('city id'),
    )

    category = forms.ModelChoiceField(
        required=False,
        queryset=IndustryCategory.objects.all(),
        label='Sector',
        empty_label=_('all sector'),
    )

    company_search = forms.CharField(
        label=_('Company'),
        required=False,
    )

    company_id = forms.CharField(
        required=False,
        label=_('company id'),
    )

    job_type = forms.ChoiceField(
        choices=JOB_TYPE_CHOICES,
        widget=forms.Select(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        type_choices = kwargs.pop('job_type_choices')
        super().__init__(*args, **kwargs)

        if type_choices:
            self.fields['job_type'].choices = \
                (('', ''),) + type_choices


class VentureForm(ModelForm):
    name = forms.CharField(
        required=True,
        label=_('name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Company name.'),
            },
        ),
    )

    class Meta:
        model = Venture
        fields = [
            'name',
            'country',
            'state',
            'city',
            'address',
            'description_en',
            'description_es',
            'industry_categories',
            'url',
            'facebook_url',
            'twitter_url',
            'instagram_url',
            'linkedin_url',
            'googleplus_url',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].choices = ()
        self.fields['city'].choices = ()

    def clean(self):
        cleaned_data = super().clean()

        description_en = cleaned_data.get('description_en')
        description_es = cleaned_data.get('description_es')

        if not description_en and not description_es:
            raise forms.ValidationError(
                _('you must add the description of your company in at least one language.')
            )


class CompanyLogoForm(Form):
    logo = forms.ImageField()


class VentureDescriptionForm(Form):
    description_en = forms.CharField(
        required=False,
        min_length=40,
        label=_('English description'),
        widget=forms.Textarea,
    )

    description_es = forms.CharField(
        required=False,
        min_length=40,
        label=_('Spanish description'),
        widget=forms.Textarea,
    )


class ContactVentureForm(ModelForm):
    class Meta:
        model = Venture
        fields = [
            'email',
            'phone_number',
        ]


class SocialMediaVentureForm(ModelForm):
    class Meta:
        model = Venture
        fields = [
            'url',
            'facebook_url',
            'twitter_url',
            'instagram_url',
            'linkedin_url',
            'googleplus_url',
        ]


class LocationVentureForm(ModelForm):
    class Meta:
        model = Venture
        fields = [
            'country',
            'state',
            'city',
            'address',
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


class RoleVentureForm(Form):
    venture_slug = forms.CharField(
        widget=forms.HiddenInput,
        label='',
    )

    profile_slug = forms.CharField(
        widget=forms.HiddenInput,
        label='',
    )
    role = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=ADMINISTRATOR_ROLES,
    )


class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = (
            'title',
            'job_type',
            'description',
            'industry_categories',
            'country',
            'state',
            'city',
        )

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get('country')
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')

        if state.country != country:
            raise forms.ValidationError('Select a state of the selected country.')

        if city.state != state:
            raise forms.ValidationError('Select a city of the selected state.')


class TransferCompany(forms.ModelForm):
    class Meta:
        model = Venture
        fields = (
            'owner',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get('instance', None)

        # Get active memverships available to translate the company.
        memberships = self.instance.administratormembership_set.filter(
            status=ACTIVE_MEMBERSHIP,
        ).exclude(admin__id=self.instance.owner.id)

        administrator_ids = list(
            memberships.values_list('admin__id', flat=True)
        )

        # Set valid professional profiles to transfer the membership.
        queryset = ProfessionalProfile.objects.filter(
            administratormembership__admin__in=administrator_ids,
        )

        # Change owner field queryet.
        self.fields['owner'].queryset = queryset

    def clean_owner(self):
        data = self.cleaned_data['owner']

        if not AdministratorMembership.objects.filter(
            venture=self.instance,
            admin=data,
            status=ACTIVE_MEMBERSHIP,
        ):
            raise forms.ValidationError(
                _('User can not be selected as owner.')
            )

        return data


class DeleteObjectMessageForm(Form):
    """
    Used to let users to send a message to platform
    administrators when they want to delete a company
    or an account.
    """
    message = forms.CharField(
        required=False,
        label=_('message'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('How can be Queryjane a better app?'),
            },
        ),
    )
