from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import View

from .permissions import AdminPermissions
from app.mixins import CustomUserMixin
from entrepreneur.data import JOB_STATUS_ACTIVE
from entrepreneur.data import VENTURE_STATUS_ACTIVE
from entrepreneur.models import JobOffer
from entrepreneur.models import Venture
from corporative.tasks import share_company_on_twitter
from corporative.tasks import share_job_on_twitter


class AdminDashboardView(CustomUserMixin, TemplateView):
    template_name = 'corporative/admin_dashboard.html'

    def test_func(self):
        return AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unshared_ventures_list = Venture.objects.filter(
            status=VENTURE_STATUS_ACTIVE,
            shared_on_twitter=False
        )

        unshared_jobs_list = JobOffer.objects.filter(
            status=JOB_STATUS_ACTIVE,
            shared_on_twitter=False
        )

        context['unshared_ventures_list'] = unshared_ventures_list
        context['unshared_jobs_list'] = unshared_jobs_list

        return context


class TwitterShareVentureView(CustomUserMixin, View):
    def test_func(self):
        return AdminPermissions.can_share_venture_twitter(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        share_company_on_twitter(self.get_object())

        return HttpResponse('success')


class TwitterShareJobView(CustomUserMixin, View):
    def test_func(self):
        return AdminPermissions.can_share_job_twitter(
            user=self.request.user,
            job=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        share_job_on_twitter(self.get_object())

        return HttpResponse('success')
