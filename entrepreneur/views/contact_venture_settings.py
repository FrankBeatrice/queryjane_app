from django.contrib.gis.geos import Point
from django.db import transaction
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import View

from app.mixins import CustomUserMixin
from entrepreneur.forms import ContactVentureForm
from entrepreneur.forms import SocialMediaVentureForm
from entrepreneur.forms import LocationVentureForm
from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions
from place.models import City
from place.models import Country


class ContactVentureFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/contact_venture_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get(self, *args, **kwargs):
        venture = self.get_object()
        contact_form = ContactVentureForm(instance=venture)
        media_form = SocialMediaVentureForm(instance=venture)
        location_form = LocationVentureForm(instance=venture)

        return self.render_to_response(
            self.get_context_data(
                venture=venture,
                country_instance=venture.country,
                contact_form=contact_form,
                media_form=media_form,
                location_form=location_form,
                contact_active=True,
            )
        )


class AjaxContactVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, id=self.kwargs.get('pk'))

    @transaction.atomic
    def post(self, request, **kwargs):
        contact_form = ContactVentureForm(
            request.POST,
        )

        if contact_form.is_valid():
            venture = self.get_object()

            email = contact_form.cleaned_data['email']
            phone_number = contact_form.cleaned_data['phone_number']

            venture.email = email
            venture.phone_number = phone_number
            venture.save()
            return HttpResponse('success')
        else:
            return HttpResponse('fail')

        raise Http404


class AjaxLocationVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, id=self.kwargs.get('pk'))

    @transaction.atomic
    def post(self, request, **kwargs):
        venture = self.get_object()

        location_form = LocationVentureForm(
            request.POST,
            instance=venture,
        )

        if location_form.is_valid():
            country_code = location_form.cleaned_data['country_code']
            city_id = location_form.cleaned_data['city_id']
            address = location_form.cleaned_data['address']
            coordinates = location_form.cleaned_data['coordinates']

            country_instance = get_object_or_404(
                Country,
                country=country_code,
            )

            city = get_object_or_404(
                City,
                id=int(city_id),
            )

            latitude = None
            longitude = None
            point = None

            if coordinates:
                latitude, longitude = coordinates.split(',')
                point = Point(float(latitude), float(longitude))

            venture.country = country_instance
            venture.city = city
            venture.address = address
            venture.coordinates = point
            venture.save()

            return HttpResponse('success')
        else:
            return HttpResponse('fail')

        raise Http404
