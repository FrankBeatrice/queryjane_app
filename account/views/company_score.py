from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.template.loader import render_to_string

from account.forms import CompanyScoreForm
from account.permissions import CompanyScorePermissions
from app.mixins import CustomUserMixin
from entrepreneur.models import Venture
from entrepreneur.models import CompanyScore


class CompanyScoreFormView(CustomUserMixin, FormView):
    form_class = CompanyScoreForm

    def get_object(self):
        return get_object_or_404(
            Venture,
            pk=self.kwargs['pk'],
        )

    def test_func(self):
        return CompanyScorePermissions.can_add_score(
            user=self.request.user,
            company=self.get_object(),
        )

    @transaction.atomic
    def form_valid(self, form):
        company = self.get_object()

        company_score = CompanyScore.objects.create(
            user=self.request.user,
            company=company,
            score=form.cleaned_data['score'],
            comment=form.cleaned_data['comment'],
        )

        if company.get_votes_quantity == 1:
            message = '1 user has scored {}.'.format(company.name)
        else:
            message = '{0} user have scored {1}.'.format(
                company.get_votes_quantity,
                company.name,
            )

        return JsonResponse(
            {
                'new_score': company.get_score,
                'message': message,
                'score_line': render_to_string(
                    'entrepreneur/company_score_line.html', {
                        'company_score': company_score,
                    },
                )
            }
        )

    def get(self, *args, **kwargs):
        raise Http404('Method not available')
