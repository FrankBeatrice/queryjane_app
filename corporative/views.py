from django.views.generic import TemplateView

from app.mixins import CustomUserMixin
from .permissions import AdminPermissions
from entrepreneur.models import Venture
from entrepreneur.models import JobOffer


class AdminDashboardView(CustomUserMixin, TemplateView):
    template_name = 'corporative/admin_dashboard.html'

    def test_func(self):
        return AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unshared_ventures_list = Venture.objects.filter(
            is_active=True,
            shared_on_twitter=False
        )

        unshared_jobs_list = JobOffer.objects.filter(
            is_active=True,
            shared_on_twitter=False
        )

        context['unshared_ventures_list'] = unshared_ventures_list
        context['unshared_jobs_list'] = unshared_jobs_list

        return context
