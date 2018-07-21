from account.models import User
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import View

from account.forms import SignUpForm
from account.forms import CompanyScoreForm
from account.models import ProfessionalProfile
from account.models import Conversation
from account.models import UserNotification
from account.permissions import AddressBookPermissions
from account.permissions import CompanyScorePermissions
from account.permissions import JobOfferPermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email
from corporative.forms import ContactForm
from entrepreneur.data import JOB_STATUS_ACTIVE
from entrepreneur.data import JOB_STATUS_CLOSED
from entrepreneur.data import JOB_TYPE_CHOICES
from entrepreneur.data import VENTURE_STATUS_ACTIVE
from entrepreneur.forms import JobOffersFilter
from entrepreneur.forms import VentureFilter
from entrepreneur.models import Applicant
from entrepreneur.models import JobOffer
from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions
from place.utils import get_user_country


class LandingPageView(TemplateView):
    """
    Application landing page, main information can be
    viewed in this page. The application domain 'queryjane.net'
    renders this view. Authenticated users are redirected to
    the dashboard page.
    """
    template_name = 'landing_page.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect autenticated users to the dashboard.
        if request.user.is_authenticated:
            return redirect('dashboard')

        else:
            return super().dispatch(request, *args, **kwargs)


class SignupView(FormView):
    """
    Form view to manage post request of the sign up form.
    An instance of the 'User' model is created and an instance
    of the 'ProfessionalProfile' model is created and linked
    the the new 'User' instance.
    """
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('account:signup_landing')

    def get(self, request, *args, **kwargs):
        # Redirect authenticated users to the landing page.
        if request.user.is_authenticated:
            return redirect('landing_page')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Get user country.
        country_instance = get_user_country(self.request.META)
        # Get registered users in the authenticated user country.
        country_users_count = User.objects.filter(
            country=country_instance,
        ).count()
        # Get registered compnies in the authenticated user country.
        country_companies_count = Venture.objects.filter(
            country=country_instance,
        ).count()

        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
            context['country'] = country_instance
            context['country_users_count'] = country_users_count
            context['country_companies_count'] = country_companies_count

        return context

    @transaction.atomic
    def form_valid(self, form):
        # Signup form post.
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Create new user instance.
        user = User.objects.create_user(
            first_name,
            last_name,
            email,
            password,
        )

        # Assing country to the user instance.
        country_instance = get_user_country(self.request.META)

        if country_instance:
            user.country = country_instance

        user.save()

        # New users are authenticated in the application.
        authenticated_user = auth.authenticate(
            username=user.email,
            password=password,
        )

        auth.login(
            self.request,
            authenticated_user,
        )

        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard view. Authenticated users are redirected to
    this page. Basic important information for the users
    is displayed in this view.
    """
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = user.professionalprofile
        user_country = user.country

        context = super().get_context_data(**kwargs)

        # Get job offers by country or interest sector.
        interest_sector_jobs = list(JobOffer.objects.filter(
            Q(country=user_country) |
            Q(industry_categories__in=profile.industry_categories.all()),
            status=JOB_STATUS_ACTIVE,
        ).exclude(
            venture_id__in=profile.get_managed_venture_ids,
        ).distinct()[:5])

        jobs_to_exclude = []

        for job_to_exclude in interest_sector_jobs:
            jobs_to_exclude.append(job_to_exclude.id)

        # Get latest publised job offers
        last_jobs = list(JobOffer.objects.filter(
            status=JOB_STATUS_ACTIVE,
        ).exclude(id__in=jobs_to_exclude)[:5])

        # Local companies
        local_companies = list(Venture.objects.filter(
            status=VENTURE_STATUS_ACTIVE,
            country=user_country,
        ).order_by('?')[:5])

        companies_to_exclude = []

        for company_to_exclude in local_companies:
            companies_to_exclude.append(company_to_exclude.id)

        # # Random companies
        random_companies = list(Venture.objects.filter(
            status=VENTURE_STATUS_ACTIVE,
        ).exclude(id__in=companies_to_exclude).order_by('?')[:5])

        # New messages
        new_conversations = Conversation.objects.filter(
            usermessage__user_to=user,
            usermessage__unread=True,
        ).distinct()

        # New messages
        new_notifications = UserNotification.objects.filter(
            noty_to=user,
            was_seen=False,
        )

        context['interest_sector_jobs'] = interest_sector_jobs
        context['last_jobs'] = last_jobs
        context['local_companies'] = local_companies
        context['random_companies'] = random_companies
        context['new_conversations'] = new_conversations
        context['new_notifications'] = new_notifications

        return context


class CompanyList(ListView):
    """
    Registered companies list. A filter form
    is avaiable in this view to search companies
    by different criteria.
    """
    model = Venture
    template_name = 'entrepreneur/company_list.html'
    context_object_name = 'company_list'

    def get_list_filter(self):
        # Get filter form with the request content as instance.
        list_filter = VentureFilter(
            self.request.GET,
        )

        return list_filter

    def get_queryset(self):
        # Return only active companies.
        queryset = Venture.objects.filter(
            status=VENTURE_STATUS_ACTIVE,
        )

        # If the filter form fields have a value, the
        # queryset is filter by this criteria.
        form = self.get_list_filter()

        if form.is_valid():
            # Filter companies by country.
            country_code = form.cleaned_data['country_code']
            if country_code:
                queryset = queryset.filter(country__country=country_code)

            # Filter companies by city.
            city_id = form.cleaned_data['city_id']
            if city_id:
                queryset = queryset.filter(city__id=city_id)

            # Filter companies by caetgory.
            category = form.cleaned_data['category']
            if category:
                queryset = queryset.filter(
                    industry_categories__in=[category],
                ).distinct()

            # Filter companies by company name.
            venture_id = form.cleaned_data['venture_id']
            if venture_id:
                queryset = queryset.filter(id=venture_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_list_filter()
        return context


class CompanyDetail(DetailView):
    """
    Company detail view. This page renders the main
    information of a registered company. If user is
    authenticate and has administration permission,
    the administrator menu will be available.
    Score form is available for authenticated users.
    """
    model = Venture
    template_name = 'entrepreneur/company_detail.html'

    def get_object(self, queryset=None):
        # Get company object.
        company = get_object_or_404(
            Venture,
            slug=self.kwargs['slug'],
        )

        return company

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        user = request.user

        # Only platform administrators and company
        # administrators can view an inactive or
        # hidden company.
        if company.is_inactive or company.is_hidden:
            if user:
                if (
                    not user.is_staff and
                    not EntrepreneurPermissions.can_manage_venture(
                        self.request.user,
                        company,
                    )
                ):
                    raise Http404

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()

        # Score form. It is displayed in the company detail.
        context['score_form'] = CompanyScoreForm()

        context['company'] = company

        # True if authenticated user has a membership as
        # company administrator.
        context['can_manage'] = EntrepreneurPermissions.can_manage_venture(
            self.request.user,
            company,
        )

        # True if authenticated user does not have a membership
        # as company administrator and if the company has not been
        # added to the address book.
        context['can_add_to_address_book'] = AddressBookPermissions.can_add_company(
            self.request.user,
            company,
        )

        # True if the company is in the address book of the
        # authenticated user.
        context['can_remove_from_address_book'] = AddressBookPermissions.can_remove_company(
            self.request.user,
            company,
        )

        # True if the authenticated user does not have a membership
        # as company administrator and if there is not a previous
        # score from the user.
        context['can_add_score'] = CompanyScorePermissions.can_add_score(
            self.request.user,
            company,
        )

        return context


class JobsList(ListView):
    """
    Jobs list view. All jobs are showed in this page.
    A filter is available to search jobs by different
    criteria.
    """
    model = JobOffer
    template_name = 'entrepreneur/jobs_list.html'
    context_object_name = 'jobs_list'

    def get_list_filter(self):
        # Get filter form with the request content as instance.
        list_filter = JobOffersFilter(
            self.request.GET,
            job_type_choices=JOB_TYPE_CHOICES,
        )

        return list_filter

    def get_queryset(self):
        # Jobs queryset to return.
        queryset = JobOffer.objects.filter(
            status__in=(
                JOB_STATUS_ACTIVE,
                JOB_STATUS_CLOSED,
            ),
        )

        # If the filter form fields have a value, the
        # queryset is filter by this criteria.
        form = self.get_list_filter()

        if form.is_valid():
            # Filter jobs by country.
            country_code = form.cleaned_data['country_code']
            if country_code:
                queryset = queryset.filter(country__country=country_code)

            # Filter jobs by city.
            city_id = form.cleaned_data['city_id']
            if city_id:
                queryset = queryset.filter(city__id=city_id)

            # Filter jobs by category.
            category = form.cleaned_data['category']
            if category:
                queryset = queryset.filter(
                    industry_categories__in=[category],
                ).distinct()

            # Filter jobs by company.
            company_id = form.cleaned_data['venture_id']
            if company_id:
                queryset = queryset.filter(id=company_id)

            # Filter jobs by type.
            job_type = form.cleaned_data['job_type']
            if job_type:
                queryset = queryset.filter(job_type=job_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_list_filter()
        return context


class JobOfferDetail(DetailView):
    """
    Job offer detail view.
    """
    model = JobOffer
    template_name = 'entrepreneur/job_detail.html'

    def get_object(self):
        return get_object_or_404(
            JobOffer,
            slug=self.kwargs.get('slug'),
        )

    def get(self, request, *args, **kwargs):
        job_offer = self.get_object()
        user = request.user

        # Closed or hidden job offers are visible only
        # for platform administrators or company administrators.
        if job_offer.is_closed or job_offer.is_hidden:
            if user:
                if (
                    not user.is_staff and
                    not EntrepreneurPermissions.can_manage_venture(
                        self.request.user,
                        job_offer.venture,
                    )
                ):
                    raise Http404

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_offer = self.get_object()

        # Users can apply to job offers from the detail page.
        # If users have applied previosuly, this functionality
        # will be disbled.
        has_applied = False
        if self.request.user.is_authenticated:
            if Applicant.objects.filter(
                job_offer=job_offer,
                applicant=self.request.user.professionalprofile
            ):
                has_applied = True

        context['job_offer'] = job_offer

        # Company administrators can manage job offers.
        context['can_manage'] = EntrepreneurPermissions.can_manage_venture(
            self.request.user,
            job_offer.venture,
        )

        # Company administrators can edit job offers.
        context['can_edit'] = JobOfferPermissions.can_edit(
            self.request.user,
            job_offer,
        )

        # Job offer apply permission.
        context['can_apply'] = JobOfferPermissions.can_apply(
            self.request.user,
            job_offer,
        )
        context['has_applied'] = has_applied

        return context


class JobOfferApplyView(CustomUserMixin, View):
    """
    Ajax view to apply for a job offer.
    """
    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))

    def test_func(self):
        return JobOfferPermissions.can_apply(
            user=self.request.user,
            job_offer=self.get_object(),
        )

    def get(self, *args, **kwargs):
        job_offer = self.get_object()

        # Create applicant instance.
        Applicant.objects.create(
            job_offer=job_offer,
            applicant=self.request.user.professionalprofile
        )

        return redirect(
            'job_offer_detail',
            job_offer.slug,
        )


class ProfessionalDetail(LoginRequiredMixin, DetailView):
    """
    Professional profile view. Only authenticated users
    can have access to the users profile page.
    """
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

        # Users can have private converstions.
        can_send_message = True
        # False if users are visiting their own profile.
        if profile == self.request.user.professionalprofile:
            can_send_message = False
        context['can_send_message'] = can_send_message

        # Users can add another users to the address book from
        # their profissional profile page.
        context['can_add_to_address_book'] = AddressBookPermissions.can_add_user(
            owner=self.request.user.professionalprofile,
            user_for_add=self.get_object(),
        )

        # Users can remove users from their address book.
        context['can_remove_from_address_book'] = AddressBookPermissions.can_remove_user(
            owner=self.request.user.professionalprofile,
            user_for_remove=self.get_object(),
        )

        return context


class ContactFormView(FormView):
    """
    Contact form view. Users can send a message to the
    platform administrators. An email is sent to the
    administrators.
    """
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

        # Create email body with the information provided
        # by the users.
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

        # Send email to the registered email Address
        # of the platform administrators.
        send_email(
            subject=subject,
            body=body,
            mail_to=settings.ADMIN_EMAILS,
        )

        return redirect('contact_form_success')


# TODO: This view must be removed.
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
    """
    Logout function. Users are redirected to the landing page.
    """
    auth.logout(request)

    return redirect('landing_page')
