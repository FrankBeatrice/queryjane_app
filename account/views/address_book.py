from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.mixins import CustomUserMixin
from account.models import UserContact
from account.models import CompanyContact
from account.models import ProfessionalProfile
from account.permissions import AddressBookPermissions
from entrepreneur.models import Venture


class AddressBookView(LoginRequiredMixin, TemplateView):
    template_name = 'account/address_book/address_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = UserContact.objects.filter(
            owner=self.request.user.professionalprofile,
        )
        context['companies'] = CompanyContact.objects.filter(
            owner=self.request.user.professionalprofile,
        )

        return context


class AddUserToAddressBookView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            ProfessionalProfile,
            id=self.kwargs.get('pk'),
        )

    def test_func(self):
        return AddressBookPermissions.can_add_user(
            owner=self.request.user.professionalprofile,
            user_for_add=self.get_object(),
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        UserContact.objects.create(
            owner=self.request.user.professionalprofile,
            user_contact=self.get_object(),
        )

        return HttpResponse("success")


class RemoveUserFromAddressBookView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            ProfessionalProfile,
            id=self.kwargs.get('pk'),
        )

    def test_func(self):
        return AddressBookPermissions.can_remove_user(
            owner=self.request.user.professionalprofile,
            user_for_remove=self.get_object(),
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        UserContact.objects.filter(
            owner=self.request.user.professionalprofile,
            user_contact=self.get_object(),
        ).delete()

        return HttpResponse("success")


class AddCompanyToAddressBookView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            Venture,
            id=self.kwargs.get('pk'),
        )

    def test_func(self):
        return AddressBookPermissions.can_add_company(
            owner=self.request.user,
            company=self.get_object(),
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        CompanyContact.objects.create(
            owner=self.request.user.professionalprofile,
            company=self.get_object(),
        )

        return HttpResponse("success")


class RemoveCompanyToAddressBookView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            Venture,
            id=self.kwargs.get('pk'),
        )

    def test_func(self):
        return AddressBookPermissions.can_remove_company(
            owner=self.request.user,
            company=self.get_object(),
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        CompanyContact.objects.filter(
            owner=self.request.user.professionalprofile,
            company=self.get_object(),
        ).delete()

        return HttpResponse("success")
