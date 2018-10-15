import xlrd

from django.conf import settings

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View
from django.views.generic import FormView
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
from corporative.forms import FormBulkForm
from entrepreneur.data import JOB_STATUS_ACTIVE
from entrepreneur.data import JOB_STATUS_HIDDEN
from entrepreneur.data import VENTURE_STATUS_ACTIVE
from entrepreneur.data import VENTURE_STATUS_HIDDEN
from entrepreneur.models import JobOffer
from entrepreneur.models import Venture
from place.models import State
from place.models import City
from place.models import Country


class LegalItemView(DetailView):
    """
    User agreement, privacy policy and cookies policy
    are consireded legal items. This view showa the
    legal items detail. If the authenticated user is
    platform administrator, the edit legal item form
    will be available.
    """
    model = Venture
    template_name = 'corporative/legal_item.html'

    def get_object(self):
        # Get current legal item by slug in the url.
        return get_object_or_404(
            LegalItem,
            slug=self.kwargs.get('slug'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if user is authenticated and if user is admin.
        is_admin = AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )
        # If can edit, the edit legal item form will be available.
        context['can_edit'] = is_admin

        # Instance current legal item in the edit form.
        if is_admin:
            context['legal_item_form'] = LegalItemForm(
                instance=self.get_object(),
            )

        return context


class LegalItemFormView(CustomUserMixin, UpdateView):
    """
    Form view to update legal items. Only platform administrators
    can submit this form. Users can select if the change is very important
    and if it requires to notify all registered users about it.
    """
    form_class = LegalItemForm
    template_name = 'corporative/legal_item.html'

    def get_success_url(self):
        return reverse(
            'corporative:legal_item',
            kwargs={'slug': self.kwargs.get('slug')}
        )

    def get_object(self):
        # Get legal item by slug.
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
        # Save legal item.
        legal_item = form.save()

        # Notify users field. If the value is True, all
        # platform users will be notified about the change.
        notify_users = form.cleaned_data['notify_users']

        if notify_users:
            # Update the date in which the legal item was updated.
            legal_item.updated_at = timezone.now()

            # Notify all users about the new legal item update.
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

                # Create notification about legal item update for all
                # registered users.
                UserNotification.objects.create(
                    notification_type=notification_type,
                    noty_to=user,
                    description=description,
                )

                # Create email to notify all users about legal item update.
                body = render_to_string(
                    'corporative/emails/legal_item_update.html', {
                        'title': description,
                        'user_to': user,
                        'notification_type': notification_type,
                        'base_url': settings.BASE_URL,
                    },
                )

                # Send email.
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


class LegalItemAgreeView(LoginRequiredMixin, View):
    """
    View to accept new legal items. Users are notified
    when a legal item is updated and teh must accept the
    new terms.
    """
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        user = request.user
        item = self.kwargs.get('slug')

        # Set to True if users accept legal item updates.
        if item == 'user-agreement':
            user.accepted_terms = True
            user.accepted_terms_date = timezone.now()

            # Set notification as seen.
            UserNotification.objects.filter(
                noty_to=user,
                notification_type=UPDATED_TERMS,
            ).update(was_seen=True)

        if item == 'privacy-policy':
            user.accepted_privacy_policy = True
            user.accepted_privacy_policy_date = timezone.now()

            # Set notification as seen.
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
    """
    Platform administrators dashboard. Exclusive actions for
    administrators are found here as hide jobs or ventures
    or share companies and ventures in the official Qjane
    social networks.
    """
    template_name = 'corporative/admin_dashboard.html'

    def test_func(self):
        return AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # List of companies that have not been shared in the
        # Qjane official social networks.
        context['unshared_companies_list'] = Venture.objects.filter(
            status=VENTURE_STATUS_ACTIVE,
            shared_on_twitter=False
        )

        # List of jobs that have not been shared in the Qjane
        # official social networks.
        context['unshared_jobs_list'] = JobOffer.objects.filter(
            status=JOB_STATUS_ACTIVE,
            shared_on_twitter=False
        )

        # List of hidden companies.
        context['hidden_companies'] = Venture.objects.filter(
            status=VENTURE_STATUS_HIDDEN,
        )

        # List of hidden job offers.
        context['hidden_job_offer'] = JobOffer.objects.filter(
            status=JOB_STATUS_HIDDEN,
        )

        return context


class TwitterShareCompanyView(CustomUserMixin, View):
    """
    Ajax View to share a company detail page in the offical
    Qjane Twitter account. Only administrators can share
    companies in social networks.
    """
    def test_func(self):
        return AdminPermissions.can_share_company_twitter(
            user=self.request.user,
            company=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        share_company_on_twitter(self.get_object())

        return HttpResponse('success')


class TwitterShareJobView(CustomUserMixin, View):
    """
    Ajax View to share a job offer detail page in the offical
    Qjane Twitter account. Only administrators can share
    job offers in social networks.
    """
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


class HideCompanyView(CustomUserMixin, View):
    """
    Ajax View to hide a company in the platform. Companies
    can be hidden if they do not fit with the platform
    standards. Only administrators can hide companies.
    """
    def test_func(self):
        return AdminPermissions.can_hide_company(
            user=self.request.user,
            company=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        company = self.get_object()
        company.status = VENTURE_STATUS_HIDDEN
        company.save()

        return HttpResponse('Hidden')


class ActivateCompanyView(CustomUserMixin, View):
    """
    Ajax view to activate a company. Only platform
    administrators can activate hidden coampanies.
    """
    def test_func(self):
        return AdminPermissions.can_activate_company(
            user=self.request.user,
            company=self.get_object(),
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
    """
    Ajax View to hide a job offer in the platform.
    Job offers can be hidden if they do not fit with
    the platform standards. Only administrators can
    hide job offers.
    """
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
    """
    Ajax view to activate a job offer. Only platform
    administrators can activate hidden job offers.
    """
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


class CityBulkFormView(CustomUserMixin, FormView):
    form_class = FormBulkForm
    template_name = 'corporative/city_bulk_form.html'
    success_url = reverse_lazy('corporative:admin_dashboard')

    def test_func(self):
        return AdminPermissions.can_manage_admin_views(
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    @transaction.atomic
    def form_valid(self, form):
        file = form.cleaned_data['excel_file']
        country_code = form.cleaned_data['country_code']

        country = Country.objects.get(country=country_code)

        # Read xls file to create economic activities instances.
        book = xlrd.open_workbook(file_contents=file.read())
        first_sheet = book.sheet_by_index(0)

        num_rows = first_sheet.nrows

        for row_idx in range(0, num_rows):
            state = first_sheet.cell(row_idx, 0).value
            state = str(state).title()

            city = first_sheet.cell(row_idx, 1).value
            city = str(city).title()

            state_instance = State.objects.get_or_create(
                name=state,
                country=country,
            )[0]

            City.objects.get_or_create(
                name=city,
                country=country,
                state=state_instance,
            )

        return super().form_valid(form)
