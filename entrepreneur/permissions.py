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
