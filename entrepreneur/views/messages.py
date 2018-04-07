from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from entrepreneur.models import Venture
from account.models import UserMessage
from entrepreneur.permissions import EntrepreneurPermissions
from app.mixins import CustomUserMixin


class MessagesView(CustomUserMixin, ListView):
    model = UserMessage
    template_name = 'entrepreneur/venture_settings/messages.html'
    context_object_name = 'messages_list'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venture'] = self.get_object()

        return context

    def get_queryset(self):
        return UserMessage.objects.filter(
            company_to=self.get_object(),
        )
