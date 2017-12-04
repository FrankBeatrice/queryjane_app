from .models import AdministratorMembership
from .data import ACTIVE_MEMBERSHIP


class EntrepreneurPermissions(object):
    @classmethod
    def can_manage_venture(self, user, venture):
        if not user.is_authenticated:
            return False

        if AdministratorMembership.objects.filter(
            admin=user.professionalprofile,
            venture=venture,
            status=ACTIVE_MEMBERSHIP,
        ):
            return True

        return False
