from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions
from app.mixins import CustomUserMixin


class PrivacyVentureFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/privacy_venture_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get(self, *args, **kwargs):
        venture = self.get_object()

        return self.render_to_response(
            self.get_context_data(
                venture=venture,
                privacy_active=True,
            )
        )
