from django.utils.translation import ugettext as _


OWNER = 10
QJANE_ADMIN = 20
QJANE_SELLER = 30

ADMINISTRATOR_ROLES = (
    (OWNER, _('Owner')),
    (QJANE_ADMIN, _('Administrator')),
)


SENT_INVITATION = 10
ACTIVE_MEMBERSHIP = 20
DEACTIVATED_MEMBERSHIP = 30
REJECTED_MEMBERSHIP = 40

MEMBERSHIP_STATUS_CHOICES = (
    (SENT_INVITATION, _('Pending membership')),
    (ACTIVE_MEMBERSHIP, _('Active membership')),
    (DEACTIVATED_MEMBERSHIP, _('Inactive membership')),
    (REJECTED_MEMBERSHIP, _('Rejected membership')),
)

VENTURE_STATUS_ACTIVE = 100
VENTURE_STATUS_INACTIVE = 120
VENTURE_STATUS_HIDDEN = 130

VENTURE_STATUS_CHOICES = (
    (VENTURE_STATUS_ACTIVE, _('Active')),
    (VENTURE_STATUS_INACTIVE, _('Inactive')),
    (VENTURE_STATUS_HIDDEN, _('Hidden')),
)

JOB_STATUS_ACTIVE = 100
JOB_STATUS_CLOSED = 120
JOB_STATUS_HIDDEN = 130

JOB_STATUS_CHOICES = (
    (JOB_STATUS_ACTIVE, _('Active')),
    (JOB_STATUS_CLOSED, _('Closed')),
    (JOB_STATUS_HIDDEN, _('Hidden')),
)


FREELANCE = 100
FULL_TIME = 110
INTERNSHIP = 120
PART_TIME = 130
TEMPORARY = 140
VOLUNTEER = 150

JOB_TYPE_CHOICES = (
    (FREELANCE, _('Freelance')),
    (FULL_TIME, _('Full time')),
    (INTERNSHIP, _('Internship')),
    (PART_TIME, _('Part time')),
    (TEMPORARY, _('Temporary')),
    (VOLUNTEER, _('Volunteer')),
)
