import json

from django.db import transaction
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import View
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.gis.geos import Point

from .data import ACTIVE_MEMBERSHIP
from .data import OWNER
from .data import QJANE_ADMIN
from .forms import ContactVentureForm
from .forms import LocationVentureForm
from .forms import VentureDescriptionForm
from .forms import VentureLogoForm
from .forms import RoleVentureForm
from .forms import VentureForm
from .forms import JobOfferForm
from .models import AdministratorMembership
from .models import Venture
from .models import JobOffer
from .permissions import EntrepreneurPermissions
from account.data import NEW_ENTREPRENEUR_ADMIN
from account.data import NEW_JOB_OFFER
from account.forms import ProfileAutocompleteForm
from account.models import IndustryCategory
from account.models import ProfessionalProfile
from account.models import UserNotification
from app.mixins import CustomUserMixin
from place.utils import get_user_country
from place.models import Country
from place.models import City


class VentureFormView(LoginRequiredMixin, CreateView):
    model = Venture
    form_class = VentureForm
    template_name = 'entrepreneur/venture_settings/venture_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry_categories'] = IndustryCategory.objects.all()
        context['country_instance'] = get_user_country(self.request.META)

        return context

    def get_initial(self):
        current_country_instance = get_user_country(self.request.META)
        return {
            'country_search': current_country_instance.name,
            'country_code': current_country_instance.country.code,
        }

    @transaction.atomic
    def form_valid(self, form):
        venture = form.save(commit=False)
        slug = slugify(venture.name)

        if (
            Venture.objects.filter(slug=slug) or
            ProfessionalProfile.objects.filter(slug=slug)
        ):
            random_string = get_random_string(length=6)
            slug = '{0}-{1}'.format(
                slug,
                random_string.lower(),
            )

        country_code = form.cleaned_data['country_code']
        country_instance = get_object_or_404(
            Country,
            country=country_code,
        )

        city = get_object_or_404(
            City,
            id=int(form.cleaned_data['city_id']),
        )

        coordinates = form.cleaned_data['coordinates']
        latitude = None
        longitude = None
        point = None

        if coordinates:
            latitude, longitude = coordinates.split(',')
            point = Point(float(latitude), float(longitude))

        venture.owner = self.request.user.professionalprofile
        venture.slug = slug
        venture.country = country_instance
        venture.city = city
        venture.state = city.state
        venture.point = point
        venture.save()

        # TODO: REVISAR M2M save.
        venture.industry_categories = form.cleaned_data['industry_categories']
        venture.save()

        # Create owner membership.
        AdministratorMembership.objects.create(
            admin=venture.owner,
            venture=venture,
            role=OWNER,
            status=ACTIVE_MEMBERSHIP,
            created_by=venture.owner,
        )

        return HttpResponseRedirect(
            reverse(
                'entrepreneur:settings_venture_form',
                args=[venture.slug],
            )
        )


class SettingsVentureFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/settings_venture_form.html'

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    def get(self, *args, **kwargs):
        venture = self.get_object()

        return self.render_to_response(
            self.get_context_data(
                venture=venture,
                venture_logo_form=VentureLogoForm(),
                description_form=VentureDescriptionForm(
                    initial={
                        'description_es': venture.description_es,
                        'description_en': venture.description_en,
                    },
                ),
                industry_categories=IndustryCategory.objects.all(),
                general_active=True,
            )
        )


class UpdateVentureLogoForm(CustomUserMixin, FormView):
    form_class = VentureLogoForm

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    def form_valid(self, form):
        venture = self.get_object()
        venture.logo = form.cleaned_data['logo']
        venture.save()

        return JsonResponse({'content': venture.get_logo})


class VentureCategoryView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        venture = self.get_object()

        category_id = request.POST.get('category_id')
        new_status = request.POST.get('new_status')
        new_status = json.loads(new_status)

        category = get_object_or_404(
            IndustryCategory,
            id=category_id,
        )

        if (
            venture.industry_categories.count() == 1 and
            not new_status
        ):
            return HttpResponse('minimum_error')

        if new_status:
            venture.industry_categories.add(category)
        else:
            venture.industry_categories.remove(category)
        venture.save()

        return HttpResponse('success')


class UpdateVentureDescriptionForm(CustomUserMixin, FormView):
    form_class = VentureDescriptionForm

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    def form_valid(self, form):
        venture = self.get_object()
        description_es = form.cleaned_data['description_es']
        description_en = form.cleaned_data['description_en']

        updated_es = False
        if venture.description_es != description_es:
            updated_es = True
            venture.description_es = description_es

        updated_en = False
        if venture.description_en != description_en:
            updated_en = True
            venture.description_en = description_en

        venture.save()

        return JsonResponse(
            {
                'content': {
                    'updated_es': updated_es,
                    'description_es': venture.description_es,
                    'updated_en': updated_en,
                    'description_en': venture.description_en,
                },
            },
        )


class ContactVentureFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/contact_venture_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get(self, *args, **kwargs):
        venture = self.get_object()
        contact_form = ContactVentureForm(instance=venture)
        location_form = LocationVentureForm(instance=venture)

        return self.render_to_response(
            self.get_context_data(
                venture=venture,
                country_instance=venture.country,
                contact_form=contact_form,
                location_form=location_form,
                contact_active=True,
            )
        )


class AjaxContactVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, id=self.kwargs.get('pk'))

    @transaction.atomic
    def post(self, request, **kwargs):
        contact_form = ContactVentureForm(
            request.POST,
        )

        if contact_form.is_valid():
            venture = self.get_object()

            email = contact_form.cleaned_data['email']
            phone_number = contact_form.cleaned_data['phone_number']

            venture.email = email
            venture.phone_number = phone_number
            venture.save()
            return HttpResponse('success')
        else:
            return HttpResponse('fail')

        raise Http404


class AjaxLocationVentureFormView(CustomUserMixin, View):
    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, id=self.kwargs.get('pk'))

    @transaction.atomic
    def post(self, request, **kwargs):
        venture = self.get_object()

        location_form = LocationVentureForm(
            request.POST,
            instance=venture,
        )

        if location_form.is_valid():
            country_code = location_form.cleaned_data['country_code']
            city_id = location_form.cleaned_data['city_id']
            address = location_form.cleaned_data['address']
            coordinates = location_form.cleaned_data['coordinates']

            country_instance = get_object_or_404(
                Country,
                country=country_code,
            )

            city = get_object_or_404(
                City,
                id=int(city_id),
            )

            latitude = None
            longitude = None
            point = None

            if coordinates:
                latitude, longitude = coordinates.split(',')
                point = Point(float(latitude), float(longitude))

            venture.country = country_instance
            venture.city = city
            venture.address = address
            venture.coordinates = point
            venture.save()

            return HttpResponse('success')
        else:
            return HttpResponse('fail')

        raise Http404


class RolesVentureFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/roles_venture_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get(self, *args, **kwargs):
        venture = self.get_object()

        memberships = venture.administratormembership_set.all()

        return self.render_to_response(
            self.get_context_data(
                venture=venture,
                memberships=memberships,
                userprofile_form=ProfileAutocompleteForm(prefix='role'),
                roles_active=True,
            )
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        membership_form = RoleVentureForm(
            request.POST,
        )

        if membership_form.is_valid():
            profile_slug = membership_form.cleaned_data['profile_slug']
            venture_slug = membership_form.cleaned_data['venture_slug']
            role = int(membership_form.cleaned_data['role'])

            profile = get_object_or_404(
                ProfessionalProfile,
                slug=profile_slug,
            )

            venture = get_object_or_404(
                Venture,
                slug=venture_slug,
            )

            if AdministratorMembership.objects.filter(
                admin=profile,
                venture=venture,
            ):
                return HttpResponse('registered-membership')

            membership = AdministratorMembership.objects.create(
                admin=profile,
                venture=venture,
                role=role,
                created_by=request.user.professionalprofile,
            )

            UserNotification.objects.create(
                notification_type=NEW_ENTREPRENEUR_ADMIN,
                noty_to=profile.user,
                venture_from=venture,
                description='Invitation to administer company from {}.'.format(
                    self.request.user.professionalprofile,
                ),
                created_by=self.request.user.professionalprofile,
                membership=membership,
            )

            return JsonResponse({'content': render_to_string(
                'entrepreneur/venture_settings/_membership_line.html',
                context={
                    'membership': membership,
                },
                request=self.request,
            )})

        else:
            return HttpResponse('fail')

        raise Http404


class JobOffersListView(CustomUserMixin, ListView):
    model = JobOffer
    template_name = 'entrepreneur/venture_settings/jobs_list.html'
    context_object_name = 'job_offers_list'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get_queryset(self):
        queryset = JobOffer.objects.filter(
            venture=self.get_object()
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venture'] = self.get_object()
        context['jobs_active'] = True

        return context


class JobOfferFormView(CustomUserMixin, CreateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'entrepreneur/venture_settings/job_form.html'

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry_categories'] = IndustryCategory.objects.all()
        context['country_instance'] = get_user_country(self.request.META)
        context['venture'] = self.get_object()
        context['jobs_active'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        venture = self.get_object()
        job_offer = form.save(commit=False)
        slug = slugify(job_offer.title)

        if JobOffer.objects.filter(slug=slug):
            random_string = get_random_string(length=6)
            slug = '{0}-{1}'.format(
                slug,
                random_string.lower(),
            )

        country_instance = None
        state = None
        city = None

        country_code = form.cleaned_data['country_code']

        if country_code:
            country_instance = get_object_or_404(
                Country,
                country=country_code,
            )

        city_id = form.cleaned_data['city_id']

        if city_id:
            city = get_object_or_404(
                City,
                id=int(form.cleaned_data['city_id']),
            )

            state = city.state

        job_offer.venture = venture
        job_offer.slug = slug
        job_offer.country = country_instance
        job_offer.city = city
        job_offer.state = state
        job_offer.save()

        job_offer.industry_categories = form.cleaned_data['industry_categories']
        job_offer.save()

        # Create potential applicants notifications.
        potential_applicants = ProfessionalProfile.objects.filter(
            industry_categories__in=job_offer.industry_categories.all(),
        )

        if job_offer.country:
            potential_applicants = potential_applicants.filter(
                user__country=job_offer.country,
            )

        if job_offer.city:
            potential_applicants = potential_applicants.filter(
                user__city=job_offer.city,
            )

        for profile in potential_applicants.all():
            UserNotification.objects.create(
                notification_type=NEW_JOB_OFFER,
                noty_to=profile.user,
                answered=True,
                venture_from=venture,
                job_offer=job_offer,
                description='New job offer that may interest you published by {}.'.format(
                    venture,
                ),
                created_by=self.request.user.professionalprofile,
            )

        return HttpResponseRedirect(
            reverse(
                'entrepreneur:job_offers_list',
                args=[self.get_object().slug],
            )
        )


class JobOfferDetail(DetailView):
    model = JobOffer
    template_name = 'entrepreneur/job_detail.html'

    def get_object(self):
        return get_object_or_404(JobOffer, slug=self.kwargs.get('slug'))


class MembershipLineView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        profile_id = request.POST.get('profile_id')
        venture_slug = request.POST.get('venture_slug')
        userprofile = get_object_or_404(
            ProfessionalProfile,
            id=profile_id,
        )

        return JsonResponse({'content': render_to_string(
            'entrepreneur/venture_settings/_userprofile_line.html',
            context={
                'userprofile': userprofile,
                'role_form': RoleVentureForm(
                    initial={
                        'venture_slug': venture_slug,
                        'profile_slug': userprofile.slug,
                        'role': QJANE_ADMIN,
                    },
                ),
            },
            request=self.request,
        )})


class PrivacyVentureFormView(LoginRequiredMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/privacy_venture_form.html'

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


def venture_as_JSON(venture):
    name = '{0} ({1})'.format(
        venture.name,
        venture.country,
    )

    return {
        'id': venture.id,
        'name': name,
    }


class VentureSearch(View):
    def get(self, request, *args, **kwargs):
        venture_list = []
        if 'q' in request.GET and request.GET.get('q'):
            query = request.GET.get('q')
            query_set = Venture.objects.filter(
                name__icontains=query
            ).distinct()

            for venture in query_set:
                venture_list.append(venture_as_JSON(venture))

        return JsonResponse(venture_list, safe=False)
