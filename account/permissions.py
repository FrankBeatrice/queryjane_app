from account.models import UserNotification
from entrepreneur.models import AdministratorMembership
from account.data import NEW_ENTREPRENEUR_ADMIN
from entrepreneur.data import SENT_INVITATION
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import OWNER
from entrepreneur.data import QJANE_ADMIN


class NotificationPermissions(object):
    @classmethod
    def can_answer_admin_invitation(self, user, venture):
        if UserNotification.objects.filter(
            notification_type=NEW_ENTREPRENEUR_ADMIN,
            noty_to=user,
            venture_from=venture,
            answered=False,
            membership__status=SENT_INVITATION,
        ):
            return True

        return False

    @classmethod
    def can_resend_admin_invitation(self, user, venture):
        if AdministratorMembership.objects.filter(
            admin=user.professionalprofile,
            venture=venture,
            status=ACTIVE_MEMBERSHIP,
            role__in=(OWNER, QJANE_ADMIN),
        ):
            return True

        return False
