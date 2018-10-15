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


class ContactCompanyFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/contact_company_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object()
        )

    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug'),
        )

    def get(self, *args, **kwargs):
        company = self.get_object()
        contact_form = ContactVentureForm(instance=company)
        media_form = SocialMediaVentureForm(instance=company)
        location_form = LocationVentureForm(instance=company)

        return self.render_to_response(
            self.get_context_data(
                company=company,
                country_instance=company.country,
                contact_form=contact_form,
                media_form=media_form,
                location_form=location_form,
                contact_active=True,
            )
        )


class AjaxContactVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object(),
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


class AjaxMediaVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, id=self.kwargs.get('pk'))

    @transaction.atomic
    def post(self, request, **kwargs):
        media_form = SocialMediaVentureForm(
            request.POST,
        )

        if media_form.is_valid():
            venture = self.get_object()
            venture.url = media_form.cleaned_data['url']
            venture.facebook_url = media_form.cleaned_data['facebook_url']
            venture.twitter_url = media_form.cleaned_data['twitter_url']
            venture.instagram_url = media_form.cleaned_data['instagram_url']
            venture.linkedin_url = media_form.cleaned_data['linkedin_url']
            venture.googleplus_url = media_form.cleaned_data['googleplus_url']
            venture.save()
            return HttpResponse('success')
        else:
            return HttpResponse('fail')

        raise Http404


class AjaxLocationVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object(),
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
            location_form.save()

            return HttpResponse('success')
        else:
            return HttpResponse('fail')

        raise Http404
