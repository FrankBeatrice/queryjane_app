from django.views.generic import TemplateView

from app.mixins import CustomUserMixin
from .permissions import AdminPermissions


class AdminDashboardView(CustomUserMixin, TemplateView):
    template_name = 'corporative/admin_dashboard.html'

    def test_func(self):
        return AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
