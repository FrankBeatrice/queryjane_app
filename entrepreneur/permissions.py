from .models import AdministratorMembership
from .data import ACTIVE_MEMBERSHIP


class EntrepreneurPermissions(object):
    @classmethod
    def can_manage_company(self, user, company):
        if not user.is_authenticated:
            return False

        if AdministratorMembership.objects.filter(
            admin=user.professionalprofile,
            venture=company,
            status=ACTIVE_MEMBERSHIP,
        ):
            return True

        return False

    @classmethod
    def can_transfer_company(self, user, company):
        if company.owner != user.professionalprofile:
            return False

        if AdministratorMembership.objects.filter(
            venture=company,
            status=ACTIVE_MEMBERSHIP,
        ).exclude(admin__id=user.professionalprofile.id):
            return True

        return False

    @classmethod
    def can_delete_company(self, user, company):
        """
        Only company owner can delete it.
        """
        if company.owner == user.professionalprofile:
            return True

        return False

    @classmethod
    def can_delete_membership(self, user, membership):
        professional_profile = user.professionalprofile

        if not AdministratorMembership.objects.filter(
            admin=user.professionalprofile,
            venture=membership.venture,
            status=ACTIVE_MEMBERSHIP,
        ):
            return False

        # Owner membership can't be deleted.
        if membership.admin == membership.venture.owner:
            return False

        # Users can delete their own membership.
        if professional_profile == membership.admin:
            return True

        # Company owner can delete all memberships.
        if professional_profile == membership.venture.owner:
            return True

        return False
