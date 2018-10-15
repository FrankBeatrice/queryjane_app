from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.views.generic import CreateView
from django.views.generic import View

from account.models import IndustryCategory
from account.models import ProfessionalProfile
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import OWNER
from entrepreneur.forms import VentureForm
from entrepreneur.models import AdministratorMembership
from entrepreneur.models import Venture
from place.utils import get_user_country


class VentureFormView(LoginRequiredMixin, CreateView):
    model = Venture
    form_class = VentureForm
    template_name = 'entrepreneur/venture_settings/venture_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry_categories'] = IndustryCategory.objects.all()
        context['country_instance'] = get_user_country(self.request.META)

        return context

    @transaction.atomic
    def form_invalid(self, form):
        print("form.errors")
        print(form.errors)

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

        venture.owner = self.request.user.professionalprofile
        venture.slug = slug
        venture.save()

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
                'entrepreneur:general_venture_form',
                args=[venture.slug],
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


class CompanySearch(View):
    def get(self, request, *args, **kwargs):
        company_list = []
        if 'q' in request.GET and request.GET.get('q'):
            query = request.GET.get('q')
            query_set = Venture.objects.filter(
                name__icontains=query
            ).distinct()

            for venture in query_set:
                company_list.append(venture_as_JSON(venture))

        return JsonResponse(company_list, safe=False)
