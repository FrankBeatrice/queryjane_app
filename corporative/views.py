from django.conf import settings

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View
from django.template.loader import render_to_string

from .models import LegalItem
from .permissions import AdminPermissions
from account.data import UPDATED_PRIVACY_POLICY
from account.data import UPDATED_TERMS
from account.models import User
from account.models import UserNotification
from app.tasks import send_email
from app.mixins import CustomUserMixin
from corporative.forms import LegalItemForm
from corporative.tasks import share_company_on_twitter
from corporative.tasks import share_job_on_twitter
from entrepreneur.data import JOB_STATUS_ACTIVE
from entrepreneur.data import JOB_STATUS_HIDDEN
from entrepreneur.data import VENTURE_STATUS_ACTIVE
from entrepreneur.data import VENTURE_STATUS_HIDDEN
from entrepreneur.models import JobOffer
from entrepreneur.models import Venture


class LegalItemView(DetailView):
    model = Venture
    template_name = 'corporative/legal_item.html'

    def get_object(self):
        return get_object_or_404(
            LegalItem,
            slug=self.kwargs.get('slug'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_admin = AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )
        context['can_edit'] = is_admin

        if is_admin:
            context['legal_item_form'] = LegalItemForm(
                instance=self.get_object(),
            )

        return context


class LegalItemFormView(CustomUserMixin, UpdateView):
    form_class = LegalItemForm
    template_name = 'corporative/legal_item.html'

    def get_success_url(self):
        return reverse(
            'corporative:legal_item',
            kwargs={'slug': self.kwargs.get('slug')}
        )

    def get_object(self):
        return get_object_or_404(
            LegalItem,
            slug=self.kwargs.get('slug'),
        )

    def test_func(self):
        return AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('landing_page')

        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        legal_item = form.save()
        notify_users = form.cleaned_data['notify_users']

        if notify_users:
            legal_item.updated_at = timezone.now()

            for user in User.objects.all():
                if legal_item.slug == 'privacy-policy':
                    user.accepted_privacy_policy = False
                    notification_type = UPDATED_PRIVACY_POLICY
                    description = 'Our privacy policy has been updated.'

                elif legal_item.slug == 'user-agreement':
                    user.accepted_terms = False
                    notification_type = UPDATED_TERMS
                    description = 'Our user agreement has been updated.'

                user.save()

                UserNotification.objects.create(
                    notification_type=notification_type,
                    noty_to=user,
                    description=description,
                )

                body = render_to_string(
                    'corporative/emails/legal_item_update.html', {
                        'title': description,
                        'user_to': user,
                        'notification_type': notification_type,
                        'base_url': settings.BASE_URL,
                    },
                )

                send_email(
                    subject=description,
                    body=body,
                    mail_to=[user.email],
                )

        legal_item.save()

        messages.success(
            self.request,
            _('legal item has been successfully updated.')
        )

        return super().form_valid(form)


class LegalItemsAgreeView(LoginRequiredMixin, View):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        user = request.user

        item = self.kwargs.get('slug')

        if item == 'user-agreement':
            user.accepted_terms = True
            user.accepted_terms_date = timezone.now()

            UserNotification.objects.filter(
                noty_to=user,
                notification_type=UPDATED_TERMS,
            ).update(was_seen=True)

        if item == 'privacy-policy':
            user.accepted_privacy_policy = True
            user.accepted_privacy_policy_date = timezone.now()

            UserNotification.objects.filter(
                noty_to=user,
                notification_type=UPDATED_PRIVACY_POLICY,
            ).update(was_seen=True)
        user.save()

        messages.success(
            self.request,
            _(
                'Thank you. We will notify you whenever there is a '
                'change in our privacy policy or in our user agreement.'
            )
        )

        return redirect('landing_page')


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

        hidden_companies = Venture.objects.filter(
            status=VENTURE_STATUS_HIDDEN,
        )

        hidden_job_offer = JobOffer.objects.filter(
            status=JOB_STATUS_HIDDEN,
        )

        context['unshared_ventures_list'] = unshared_ventures_list
        context['unshared_jobs_list'] = unshared_jobs_list
        context['hidden_companies'] = hidden_companies
        context['hidden_job_offer'] = hidden_job_offer

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


class HideVentureView(CustomUserMixin, View):
    def test_func(self):
        return AdminPermissions.can_hide_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        venture = self.get_object()
        venture.status = VENTURE_STATUS_HIDDEN
        venture.save()

        return HttpResponse('Hidden')


class ActivateVentureView(CustomUserMixin, View):
    def test_func(self):
        return AdminPermissions.can_activate_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        venture = self.get_object()
        venture.status = VENTURE_STATUS_ACTIVE
        venture.save()

        return HttpResponse('Active')


class HideJobOfferView(CustomUserMixin, View):
    def test_func(self):
        return AdminPermissions.can_hide_job_offer(
            user=self.request.user,
            job_offer=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        job_offer = self.get_object()
        job_offer.status = JOB_STATUS_HIDDEN
        job_offer.save()

        return HttpResponse('Hidden')


class ActivateJobOfferView(CustomUserMixin, View):
    def test_func(self):
        return AdminPermissions.can_activate_job_offer(
            user=self.request.user,
            job_offer=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        job_offer = self.get_object()
        job_offer.status = JOB_STATUS_ACTIVE
        job_offer.save()

        return HttpResponse('Active')
