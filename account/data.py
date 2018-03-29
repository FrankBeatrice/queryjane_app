from django.utils.translation import ugettext as _

NEW_ENTREPRENEUR_ADMIN = 10
NEW_JOB_OFFER = 20
NEW_APPLICANTS = 30

NOTIFICATION_TYPE_CHOICES = (
    (NEW_ENTREPRENEUR_ADMIN, _('Invitation to administer company.')),
    (NEW_JOB_OFFER, _('New job offer that may interest you.')),
    (NEW_APPLICANTS, _('New applicants to my job offer.')),
)
