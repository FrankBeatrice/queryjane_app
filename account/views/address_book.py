from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AddressBookView(LoginRequiredMixin, TemplateView):
    template_name = 'account/address_book/address_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
