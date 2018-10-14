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
from place.models import City
from place.models import Country
from place.models import State


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

    coordinates = forms.CharField(
        required=False,
        label=_('coordinates'),
    )

    class Meta:
        model = Venture
        fields = [
            'name',
            'country',
            'state',
            'city',
            'address',
            'coordinates',
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

        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        city_id = cleaned_data.get('city_id')

        if not country_code:
            self.add_error(
                'country_search',
                _('Type the country name and select it from the list.'),
            )

        if not city_id:
            self.add_error(
                'city_search',
                _('Type the city name and select it from the list.'),
            )

        city = None
        country = None

        try:
            city = City.objects.get(id=int(city_id))
        except City.DoesNotExist:
            pass

        try:
            country = Country.objects.get(
                country=country_code,
            )
        except Country.DoesNotExist:
            pass

        if country and city:
            if city.country != country:
                self.add_error(
                    'city_search',
                    'select a city in {}'.format(country.name),
                )

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
    country_search = forms.CharField(
        required=True,
        label=_('Country'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type the country name and select it from the list.'),
            },
        ),
    )

    country_code = forms.CharField(
        required=True,
        label=_('country code'),
    )

    city_search = forms.CharField(
        label=_('City'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('type the city name.'),
            },
        ),
    )

    city_id = forms.CharField(
        label=_('City id'),
    )

    coordinates = forms.CharField(
        required=False,
        label=_('coordinates'),
    )

    class Meta:
        model = Venture
        fields = [
            'address',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        venture = kwargs.get('instance', None)

        self.fields['country_search'].initial = venture.country.name
        self.fields['country_code'].initial = venture.country.country.code
        self.fields['city_search'].initial = venture.city.name
        self.fields['city_id'].initial = venture.city.id

        if venture.point:
            self.fields['coordinates'].initial = '{},{}'.format(
                venture.point.coords[0],
                venture.point.coords[1],
            )

    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        city_id = cleaned_data.get('city_id')

        if not country_code:
            self.add_error(
                'country_search',
                _('Type the country name and select it from the list.'),
            )

        if not city_id:
            self.add_error(
                'city_search',
                _('Type the city name and select it from the list.'),
            )

        city = None
        country = None

        try:
            city = City.objects.get(id=int(city_id))
        except City.DoesNotExist:
            pass

        try:
            country = Country.objects.get(
                country=country_code,
            )
        except Country.DoesNotExist:
            pass

        if country and city:
            if city.country != country:
                self.add_error(
                    'city_search',
                    'Select a city in {}'.format(country.name),
                )


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
    country_search = forms.CharField(
        required=False,
        label='Country',
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

    class Meta:
        model = JobOffer
        fields = (
            'title',
            'job_type',
            'description',
            'industry_categories',
            'country_search',
            'country_code',
            'city_search',
            'city_id',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        job_offer = kwargs.get('instance', None)

        country = None
        city = None

        if job_offer:
            country = job_offer.country
            city = job_offer.city

        if country:
            self.fields['country_search'].initial = job_offer.country.name
            self.fields['country_code'].initial = job_offer.country.country.code

        if city:
            self.fields['city_search'].initial = job_offer.city.name
            self.fields['city_id'].initial = job_offer.city.id


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
