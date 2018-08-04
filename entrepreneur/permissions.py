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
