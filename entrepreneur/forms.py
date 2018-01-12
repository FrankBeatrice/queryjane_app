from django import forms
from django.forms import Form
from django.forms import ModelForm

from .models import Venture
from .models import JobOffer
from place.models import City
from place.models import Country
from .data import ADMINISTRATOR_ROLES
from account.models import IndustryCategory


class VentureFilter(forms.Form):
    country_search = forms.CharField(
        required=False,
        label='Country',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type the country name and select one from the list.',
            },
        ),
    )

    country_code = forms.CharField(
        required=False,
        label='country code',
    )

    city_search = forms.CharField(
        required=False,
        label='City',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type de city name.',
            },
        ),
    )

    city_id = forms.CharField(
        required=False,
        label='city id',
    )

    category = forms.ModelChoiceField(
        required=False,
        queryset=IndustryCategory.objects.all(),
        label='Sector',
        empty_label='all sector',
    )

    venture_search = forms.CharField(
        label='Search company',
        required=False,
    )

    venture_id = forms.CharField(
        required=False,
        label='company id',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VentureForm(ModelForm):
    name = forms.CharField(
        required=True,
        label='name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Company name.',
            },
        ),
    )

    country_search = forms.CharField(
        required=True,
        label='country',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type the contry name and select one from the list.',
            },
        ),
    )

    country_code = forms.CharField(
        required=True,
        label='country code',
    )

    city_search = forms.CharField(
        label='city',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type the city name.',
            },
        ),
    )

    city_id = forms.CharField(
        label='city id',
    )

    coordinates = forms.CharField(
        required=False,
        label='coordinates',
    )

    class Meta:
        model = Venture
        fields = [
            'name',
            'country_search',
            'country_code',
            'city_search',
            'city_id',
            'address',
            'coordinates',
            'description_en',
            'industry_categories',
        ]

    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        city_id = cleaned_data.get('city_id')

        if not country_code:
            self.add_error(
                'country_search',
                'Type the country name and select it from the list.',
            )

        if not city_id:
            self.add_error(
                'city_search',
                'Type the city name and select it from the list.',
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


class VentureLogoForm(Form):
    logo = forms.ImageField()


class VentureDescriptionForm(Form):
    description_en = forms.CharField(
        required=False,
        min_length=40,
        label='description',
        widget=forms.Textarea,
    )

    description_es = forms.CharField(
        required=False,
        min_length=40,
        label='description',
        widget=forms.Textarea,
    )


class ContactVentureForm(ModelForm):
    class Meta:
        model = Venture
        fields = [
            'email',
            'phone_number',
        ]


class LocationVentureForm(ModelForm):
    country_search = forms.CharField(
        required=True,
        label='País',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type the country name and select it from the list.',
            },
        ),
    )

    country_code = forms.CharField(
        required=True,
        label='country code',
    )

    city_search = forms.CharField(
        label='City',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'type de the city name.',
            },
        ),
    )

    city_id = forms.CharField(
        label='City id',
    )

    coordinates = forms.CharField(
        required=False,
        label='coordinates',
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
                'Type the country name and select it from the list.',
            )

        if not city_id:
            self.add_error(
                'city_search',
                'Type the city name and select it from the list.',
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
                'placeholder': 'Type the country name and select one from the list.',
            },
        ),
    )

    country_code = forms.CharField(
        required=False,
        label='country code',
    )

    city_search = forms.CharField(
        required=False,
        label='City',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type de city name.',
            },
        ),
    )

    city_id = forms.CharField(
        required=False,
        label='city id',
    )

    class Meta:
        model = JobOffer
        fields = (
            'title',
            'description',
            'industry_categories',
            'country_search',
            'country_code',
            'city_search',
            'city_id',
        )
