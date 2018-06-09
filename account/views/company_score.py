from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.template.loader import render_to_string

from account.data import NEW_COMPANY_SCORE
from account.forms import CompanyScoreForm
from account.models import UserNotification
from account.permissions import CompanyScorePermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.models import CompanyScore
from entrepreneur.models import Venture


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

        for membership in company.administratormembership_set.filter(
            status=ACTIVE_MEMBERSHIP,
        ):
            subject = '{} has been scored by an user.'.format(company)
            # Create platform notification.
            UserNotification.objects.create(
                notification_type=NEW_COMPANY_SCORE,
                noty_to=membership.admin.user,
                venture_to=company,
                description=subject,
            )

            if membership.admin.new_company_scores_notifications:
                body = render_to_string(
                    'account/emails/new_company_score.html', {
                        'title': subject,
                        'user_to': membership.admin.user,
                        'company_score': company_score,
                        'base_url': settings.BASE_URL,
                    },
                )

                send_email(
                    subject=subject,
                    body=body,
                    mail_to=[membership.admin.user.email],
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
