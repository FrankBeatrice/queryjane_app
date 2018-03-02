from account.models import User
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import View

from account.forms import SignUpForm
from account.models import ProfessionalProfile
from account.models import UserMessage
from account.permissions import JobOfferPermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email
from corporative.forms import ContactForm
from entrepreneur.data import JOB_TYPE_CHOICES
from entrepreneur.forms import JobOffersFilter
from entrepreneur.forms import VentureFilter
from entrepreneur.models import Applicant
from entrepreneur.models import JobOffer
from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions
from place.utils import get_user_country


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        country_instance = get_user_country(self.request.META)
        country_users_count = User.objects.filter(
            country=country_instance,
        ).count()

        country_ventures_count = Venture.objects.filter(
            country=country_instance,
        ).count()

        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
            context['signup_form'] = SignUpForm()
            context['country'] = country_instance
            context['country_users_count'] = country_users_count
            context['country_ventures_count'] = country_ventures_count

        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = user.professionalprofile
        user_country = user.country

        context = super().get_context_data(**kwargs)
        # Get job offers by country or interest sector.
        interest_sector_jobs = JobOffer.objects.filter(
            Q(country=user_country) |
            Q(industry_categories__in=profile.industry_categories.all()),
        ).exclude(
            venture_id__in=profile.get_managed_venture_ids,
        ).distinct()[:5]

        exclude_jobs = list(interest_sector_jobs.values_list('id', flat=True))

        # Get latest publised job offers
        latest_jobs = JobOffer.objects.filter(
            is_active=True,
        ).exclude(id__in=exclude_jobs)[:5]

        # Local companies
        local_companies = Venture.objects.filter(
            is_active=True,
            country=user_country,
        ).order_by('?')[:2]

        exclude_companies = list(local_companies.values_list('id', flat=True))

        # Random companies
        random_companies = Venture.objects.filter(
            is_active=True,
        ).exclude(id__in=exclude_companies).order_by('?')[:5]

        # New messages
        new_messages = UserMessage.objects.filter(
            user_to=user,
            unread=True,
        )

        context['interest_sector_jobs'] = interest_sector_jobs
        context['lastest_jobs'] = latest_jobs
        context['local_companies'] = local_companies
        context['random_companies'] = random_companies
        context['new_messages'] = new_messages

        return context


class VentureList(ListView):
    model = Venture
    template_name = 'entrepreneur/venture_list.html'
    context_object_name = 'venture_list'

    def get_list_filter(self):
        list_filter = VentureFilter(
            self.request.GET,
        )

        return list_filter

    def get_queryset(self):
        queryset = Venture.objects.filter(is_active=True)

        form = self.get_list_filter()

        if form.is_valid():
            country_code = form.cleaned_data['country_code']
            if country_code:
                queryset = queryset.filter(country__country=country_code)

            city_id = form.cleaned_data['city_id']

            if city_id:
                queryset = queryset.filter(city__id=city_id)

            category = form.cleaned_data['category']

            if category:
                queryset = queryset.filter(
                    industry_categories__in=[category],
                ).distinct()

            venture_id = form.cleaned_data['venture_id']

            if venture_id:
                queryset = queryset.filter(id=venture_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_list_filter()
        return context


class VentureDetail(DetailView):
    model = Venture
    template_name = 'entrepreneur/venture_profile.html'

    def get_object(self, queryset=None):
        venture = get_object_or_404(
            Venture,
            slug=self.kwargs['slug'],
        )

        return venture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venture = self.get_object()

        context['venture'] = venture
        context['can_manage'] = EntrepreneurPermissions.can_manage_venture(
            self.request.user,
            venture,
        )

        return context


class JobsList(ListView):
    model = JobOffer
    template_name = 'entrepreneur/jobs_list.html'
    context_object_name = 'jobs_list'

    def get_list_filter(self):
        list_filter = JobOffersFilter(
            self.request.GET,
            job_type_choices=JOB_TYPE_CHOICES,
        )

        return list_filter

    def get_queryset(self):
        queryset = JobOffer.objects.all()

        form = self.get_list_filter()

        if form.is_valid():
            country_code = form.cleaned_data['country_code']
            if country_code:
                queryset = queryset.filter(country__country=country_code)

            city_id = form.cleaned_data['city_id']

            if city_id:
                queryset = queryset.filter(city__id=city_id)

            category = form.cleaned_data['category']

            if category:
                queryset = queryset.filter(
                    industry_categories__in=[category],
                ).distinct()

            venture_id = form.cleaned_data['venture_id']

            if venture_id:
                queryset = queryset.filter(id=venture_id)

            job_type = form.cleaned_data['job_type']

            if job_type:
                queryset = queryset.filter(job_type=job_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_list_filter()
        return context


class ProfessionalDetail(LoginRequiredMixin, DetailView):
    model = ProfessionalProfile
    template_name = 'account/professional_profile.html'

    def get_object(self, queryset=None):
        professional_profile = get_object_or_404(
            ProfessionalProfile,
            slug=self.kwargs['slug'],
        )

        return professional_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile

        can_send_message = True

        if profile == self.request.user.professionalprofile:
            can_send_message = False

        context['can_send_message'] = can_send_message

        return context


def ajax_login_form(request):
    if not request.is_ajax():
        raise Http404

    try:
        email = (request.POST['login_form-email'] or u'').lower()
        password = request.POST['login_form-password']

        user_ex = User.objects.get(email=email)

    except User.DoesNotExist:
        return HttpResponse('fail')

    user = auth.authenticate(
        username=user_ex.email,
        password=password,
    )

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponse('successful_login')
        else:
            return HttpResponse('inactive_account')

    else:
        return HttpResponse('data_error')


def user_logout(request):
    auth.logout(request)

    return redirect('home')


class JobOfferDetail(DetailView):
    model = JobOffer
    template_name = 'entrepreneur/job_detail.html'

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_offer = self.get_object()

        has_applied = False

        if self.request.user.is_authenticated:
            if Applicant.objects.filter(
                job_offer=job_offer,
                applicant=self.request.user.professionalprofile
            ):
                has_applied = True

        context['can_manage'] = EntrepreneurPermissions.can_manage_venture(
            self.request.user,
            job_offer.venture,
        )

        context['can_edit'] = JobOfferPermissions.can_edit(
            self.request.user,
            job_offer,
        )

        context['can_apply'] = JobOfferPermissions.can_apply(
            self.request.user,
            job_offer,
        )
        context['has_applied'] = has_applied

        return context


class JobOfferApplyView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    def test_func(self):
        return JobOfferPermissions.can_apply(
            user=self.request.user,
            job_offer=self.get_object(),
        )

    def get(self, *args, **kwargs):
        job_offer = self.get_object()

        Applicant.objects.create(
            job_offer=job_offer,
            applicant=self.request.user.professionalprofile
        )

        return redirect(
            'job_offer_detail',
            job_offer.slug,
        )


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'corporative/contact_form.html'

    def get_initial(self):
        initial = super().get_initial()

        user = self.request.user
        name = ''
        email = ''

        if user.is_authenticated:
            name = user.get_full_name
            email = user.email

        if user:
            initial = {
                'name': name,
                'email': email,
            }

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        phone = form.cleaned_data['phone']
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        body = render_to_string(
            'corporative/emails/user_message.html', {
                'title': subject,
                'phone': phone,
                'name': name,
                'email': email,
                'message': message,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=settings.ADMIN_EMAILS,
        )

        return redirect('contact_form_success')
