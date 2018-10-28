from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import Http404
from django.views.generic import View

from app.mixins import CustomUserMixin
from entrepreneur.permissions import EntrepreneurPermissions
from entrepreneur.models import Venture
from entrepreneur.forms import RoleVentureForm
from account.models import UserNotification
from account.forms import ProfileAutocompleteForm
from account.data import NEW_ENTREPRENEUR_ADMIN
from account.data import DELETED_MEMBERSHIP
from account.models import ProfessionalProfile
from entrepreneur.models import AdministratorMembership
from entrepreneur.data import QJANE_ADMIN


class RolesCompanyFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/roles_company_form.html'

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

    def get(self, *args, **kwargs):
        company = self.get_object()

        memberships = company.administratormembership_set.all()

        return self.render_to_response(
            self.get_context_data(
                company=company,
                memberships=memberships,
                userprofile_form=ProfileAutocompleteForm(prefix='role'),
                roles_active=True,
            )
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        company = self.get_object()

        if company.is_inactive:
            raise Http404

        membership_form = RoleVentureForm(
            request.POST,
        )

        if membership_form.is_valid():
            profile_slug = membership_form.cleaned_data['profile_slug']
            company_slug = membership_form.cleaned_data['venture_slug']
            role = int(membership_form.cleaned_data['role'])

            profile = get_object_or_404(
                ProfessionalProfile,
                slug=profile_slug,
            )

            company = get_object_or_404(
                Venture,
                slug=company_slug,
            )

            if AdministratorMembership.objects.filter(
                admin=profile,
                venture=company,
            ):
                return HttpResponse('registered-membership')

            membership = AdministratorMembership.objects.create(
                admin=profile,
                venture=company,
                role=role,
                created_by=request.user.professionalprofile,
            )

            UserNotification.objects.create(
                notification_type=NEW_ENTREPRENEUR_ADMIN,
                noty_to=profile.user,
                venture_from=company,
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


class DeleteMembershipView(CustomUserMixin, View):
    """
    Delete company membership.
    """
    def test_func(self):
        return EntrepreneurPermissions.can_delete_membership(
            user=self.request.user,
            membership=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(
            AdministratorMembership,
            id=self.kwargs.get('membership_id'),
        )

    def post(self, request, **kwargs):
        membership = self.get_object()

        noty_to = membership.admin.user
        company = membership.venture

        membership.delete()

        UserNotification.objects.create(
            notification_type=DELETED_MEMBERSHIP,
            noty_to=noty_to,
            venture_from=company,
            description='Administrator membership delete by {}.'.format(
                self.request.user.professionalprofile,
            ),
            created_by=self.request.user.professionalprofile,
        )

        return HttpResponse('success')
