from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View

from account.data import NEW_JOB_OFFER
from account.models import IndustryCategory
from account.models import ProfessionalProfile
from account.models import UserNotification
from account.permissions import JobOfferPermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email
from entrepreneur.data import JOB_STATUS_CLOSED
from entrepreneur.forms import JobOfferForm
from entrepreneur.models import JobOffer
from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions
from place.utils import get_user_country


class JobOffersListView(CustomUserMixin, ListView):
    model = JobOffer
    template_name = 'entrepreneur/venture_settings/jobs_list.html'
    context_object_name = 'job_offers_list'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug'),
        )

    def get_queryset(self):
        queryset = JobOffer.objects.filter(
            venture=self.get_object()
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.get_object()
        context['jobs_active'] = True

        return context


class JobOfferFormView(CustomUserMixin, CreateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'entrepreneur/venture_settings/job_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry_categories'] = IndustryCategory.objects.all()
        context['country_instance'] = get_user_country(self.request.META)
        context['company'] = self.get_object()
        context['jobs_active'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        company = self.get_object()

        if company.is_inactive:
            raise Http404

        job_offer = form.save(commit=False)
        slug = slugify(job_offer.title)

        if JobOffer.objects.filter(slug=slug):
            random_string = get_random_string(length=6)
            slug = '{0}-{1}'.format(
                slug,
                random_string.lower(),
            )

        job_offer.venture = company
        job_offer.slug = slug
        job_offer.save()

        job_offer.industry_categories = form.cleaned_data['industry_categories']
        job_offer.save()

        # Create potential applicants notifications.
        potential_applicants = ProfessionalProfile.objects.filter(
            industry_categories__in=job_offer.industry_categories.all(),
        ).distinct().exclude(id__in=company.get_active_administrator_ids)

        if job_offer.country:
            potential_applicants = potential_applicants.filter(
                user__country=job_offer.country,
            )

        if job_offer.city:
            potential_applicants = potential_applicants.filter(
                user__city=job_offer.city,
            )

        description = 'New job offer that may interest you published by {}.'.format(
            company,
        )

        for profile in potential_applicants.all():
            UserNotification.objects.create(
                notification_type=NEW_JOB_OFFER,
                noty_to=profile.user,
                venture_from=company,
                job_offer=job_offer,
                description=description,
                created_by=self.request.user.professionalprofile,
            )

            if profile.email_jobs_notifications:
                subject = description

                body = render_to_string(
                    'account/emails/potenitial_job_offer.html', {
                        'title': subject,
                        'profile': profile,
                        'job_offer': job_offer,
                        'base_url': settings.BASE_URL,
                    },
                )

                send_email(
                    subject=subject,
                    body=body,
                    mail_to=[profile.user.email],
                )

        return HttpResponseRedirect(
            reverse(
                'entrepreneur:job_offers_list',
                args=[self.get_object().slug],
            )
        )


class JobOfferUpdateView(CustomUserMixin, UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'entrepreneur/venture_settings/job_update.html'

    def test_func(self):
        return JobOfferPermissions.can_edit(
            self.request.user,
            self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry_categories'] = IndustryCategory.objects.all()
        context['company'] = self.get_object().venture
        context['job_offer'] = self.get_object()
        context['jobs_active'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        form.save()

        return redirect(
            self.get_object().get_absolute_url()
        )


class JobOfferCloseView(CustomUserMixin, View):
    def test_func(self):
        return JobOfferPermissions.can_edit(
            self.request.user,
            self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        job_offer = self.get_object()
        job_offer.status = JOB_STATUS_CLOSED
        job_offer.save()

        return HttpResponse('success')
