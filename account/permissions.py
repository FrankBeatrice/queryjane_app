from account.models import UserNotification
from account.models import UserContact
from account.models import CompanyContact
from entrepreneur.models import AdministratorMembership
from entrepreneur.models import Applicant
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

    @classmethod
    def can_view(self, user, notification):
        if notification.noty_to == user:
            return True

        return False


class MessagesPermissions(object):
    @classmethod
    def can_view(self, user, message):
        if message.user_to == user:
            return True

        return False


class AddressBookPermissions(object):
    @classmethod
    def can_add_user(self, owner, user_for_add):
        if owner == user_for_add:
            return False
        if not UserContact.objects.filter(
            owner=owner,
            user_contact=user_for_add,
        ):
            return True

        return False

    @classmethod
    def can_remove_user(self, owner, user_for_remove):
        if owner == user_for_remove:
            return False

        if UserContact.objects.filter(
            owner=owner,
            user_contact=user_for_remove,
        ):
            return True

        return False

    @classmethod
    def can_add_company(self, owner, company):
        if AdministratorMembership.objects.filter(
            admin=owner,
            venture=company,
            status=ACTIVE_MEMBERSHIP,
        ):
            return False

        if not CompanyContact.objects.filter(
            owner=owner,
            company=company,
        ):
            return True

        return False


class JobOfferPermissions(object):
    @classmethod
    def can_edit(self, user, job_offer):
        if not user.is_authenticated:
            return False

        if not job_offer.is_active:
            return False

        if AdministratorMembership.objects.filter(
            admin=user.professionalprofile,
            venture=job_offer.venture,
            status=ACTIVE_MEMBERSHIP,
        ):
            return True

        return False

    @classmethod
    def can_apply(self, user, job_offer):
        if not user.is_authenticated:
            return False

        if not job_offer.is_active:
            return False

        professional_profile = user.professionalprofile
        venture = job_offer.venture

        if professional_profile.id in venture.get_active_administrator_ids:
            return False

        if Applicant.objects.filter(
            job_offer=job_offer,
            applicant=professional_profile,
        ):
            return False

        return True
