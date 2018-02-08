from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import auth
from account.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from app.mixins import CustomUserMixin
from account.models import ProfessionalProfile
from entrepreneur.models import Venture
from entrepreneur.models import Applicant
from account.permissions import JobOfferPermissions
from entrepreneur.permissions import EntrepreneurPermissions
from entrepreneur.forms import VentureFilter
from entrepreneur.forms import JobOffersFilter
from entrepreneur.models import JobOffer
from place.utils import get_user_country

from account.forms import SignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                'professional_detail',
                slug=request.user.professionalprofile.slug,
            )

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

        country = None

        if country_instance:
            country = country_instance.country

        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
            context['signup_form'] = SignUpForm()
            context['country'] = country
            context['country_users_count'] = country_users_count
            context['country_ventures_count'] = country_ventures_count

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
        )

        return list_filter

    def get_queryset(self):
        queryset = JobOffer.objects.filter(is_active=True)

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

        if Applicant.objects.filter(
            job_offer=job_offer,
            applicant=self.request.user.professionalprofile
        ):
            has_applied = True

        context['can_manage'] = EntrepreneurPermissions.can_manage_venture(
            self.request.user,
            job_offer.venture,
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
