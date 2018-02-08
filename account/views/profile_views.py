import json

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View

from account.forms import AvatarForm
from account.forms import ProfileDescriptionForm
from account.forms import ProfileForm
from account.forms import SignUpForm
from account.models import IndustryCategory
from account.models import ProfessionalProfile
from account.models import User
from place.models import City
from place.models import Country
from place.utils import get_user_country


def profile_as_JSON(profile):
    name = '{0} ({1})'.format(
        profile.user.get_full_name,
        profile.slug,
    )

    return {
        'id': profile.id,
        'name': name,
    }


class ProfileSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile_list = []
        if 'q' in request.GET and request.GET.get('q'):
            query = request.GET.get('q')
            query_set = ProfessionalProfile.objects.filter(
                Q(user__email__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query),
            ).exclude(id=request.user.professionalprofile.id).distinct()

            for profile in query_set:
                profile_list.append(profile_as_JSON(profile))

        return JsonResponse(profile_list, safe=False)


class SignUpFormView(FormView):
    form_class = SignUpForm

    @transaction.atomic
    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create_user(
            first_name,
            last_name,
            email,
            password,
        )

        user.first_name = first_name
        user.last_name = last_name

        country_instance = get_user_country(self.request.META)

        if country_instance:
            user.country = country_instance

        user.save()

        authenticated_user = auth.authenticate(
            username=user.email,
            password=password,
        )

        auth.login(
            self.request,
            authenticated_user,
        )

        return HttpResponseRedirect(
            reverse('account:signup_landing')
        )


class NewUserLandingView(LoginRequiredMixin, TemplateView):
    template_name = 'account/signup_landing.html'

    def get(self, request, *args, **kwargs):
        professional_profile = request.user.professionalprofile

        if professional_profile.industry_categories.count():
            return redirect(
                'professional_detail',
                professional_profile.slug,
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry_categories'] = IndustryCategory.objects.all()

        return context


class ProfessionalProfileCategoryView(LoginRequiredMixin, View):
    def get_object(self):
        return self.request.user.professionalprofile

    @transaction.atomic
    def post(self, request, **kwargs):
        professionalprofile = self.get_object()

        category_id = request.POST.get('category_id')
        new_status = request.POST.get('new_status')
        new_status = json.loads(new_status)

        category = get_object_or_404(
            IndustryCategory,
            id=category_id,
        )

        if new_status:
            professionalprofile.industry_categories.add(category)
        else:
            professionalprofile.industry_categories.remove(category)
        professionalprofile.save()

        return HttpResponse('success')


class UpdateProfileFormView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'account/profile_update.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        professional_profile = self.get_object().professionalprofile

        context = super().get_context_data(**kwargs)
        context['professional_profile'] = professional_profile
        context['avatar_form'] = AvatarForm()
        context['industry_categories'] = IndustryCategory.objects.all()
        context['profile_description_form'] = ProfileDescriptionForm(
            initial={
                'description_es': professional_profile.description_es,
                'description_en': professional_profile.description_en,
            },
        )

        return context

    @transaction.atomic
    def form_valid(self, form):
        user = self.get_object()

        country_code = form.cleaned_data['country_code']
        country_instance = get_object_or_404(
            Country,
            country=country_code,
        )

        city = get_object_or_404(
            City,
            id=int(form.cleaned_data['city_id']),
        )

        user.country = country_instance
        user.city = city
        user.state = city.state
        user.save()

        return HttpResponse('success')


class UpdateProfileDescriptionForm(LoginRequiredMixin, FormView):
    form_class = ProfileDescriptionForm

    def get_object(self):
        return self.request.user.professionalprofile

    def form_valid(self, form):
        professional_profile = self.get_object()
        description_es = form.cleaned_data['description_es']
        description_en = form.cleaned_data['description_en']

        updated_es = False
        if professional_profile.description_es != description_es:
            updated_es = True
            professional_profile.description_es = description_es

        updated_en = False
        if professional_profile.description_en != description_en:
            updated_en = True
            professional_profile.description_en = description_en

        professional_profile.save()

        return JsonResponse(
            {
                'content': {
                    'updated_es': updated_es,
                    'description_es': professional_profile.description_es,
                    'updated_en': updated_en,
                    'description_en': professional_profile.description_en,
                },
            },
        )


class UpdateProfileAvatarForm(LoginRequiredMixin, FormView):
    form_class = AvatarForm

    def form_valid(self, form):
        user = self.request.user
        user.avatar = form.cleaned_data['avatar']
        user.save()

        return JsonResponse({'content': user.get_avatar})


class EmailNotificationsUpdateView(LoginRequiredMixin, View):
    def get_object(self):
        return self.request.user.professionalprofile

    @transaction.atomic
    def post(self, request, **kwargs):
        professionalprofile = self.get_object()

        notification = request.POST.get('notification')
        value = request.POST.get('value')

        # Value to set in notification settings.
        new_value = False
        if value == 'notify':
            new_value = True

        print("notification")
        print(notification)

        print("new_value")
        print(new_value)

        setattr(professionalprofile, notification, new_value)
        professionalprofile.save()

        return HttpResponse('success')
