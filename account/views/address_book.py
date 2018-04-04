from django.http import HttpResponse
from django.views.generic import View
from django.db import transaction
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from account.models import UserContact


class AddressBookView(LoginRequiredMixin, TemplateView):
    template_name = 'account/address_book/address_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddUserToAddressBookView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, **kwargs):
        user_to_add_id = request.POST.get('user_to_add_id')

        UserContact.objetcs.create(
            owner=self.request.user.professionalprofile,
            user_contact_id=user_to_add_id,
        )

        return HttpResponse("success")
