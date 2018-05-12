from app.validators import FileSizeValidator
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from model_utils import FieldTracker

from .data import ACTIVE_MEMBERSHIP
from .data import ADMINISTRATOR_ROLES
from .data import FREELANCE
from .data import JOB_STATUS_ACTIVE
from .data import JOB_STATUS_CHOICES
from .data import JOB_STATUS_CLOSED
from .data import JOB_STATUS_HIDDEN
from .data import JOB_TYPE_CHOICES
from .data import MEMBERSHIP_STATUS_CHOICES
from .data import QJANE_ADMIN
from .data import REJECTED_MEMBERSHIP
from .data import SENT_INVITATION
from .data import VENTURE_STATUS_ACTIVE
from .data import VENTURE_STATUS_CHOICES
from .data import VENTURE_STATUS_HIDDEN
from .data import VENTURE_STATUS_INACTIVE


class Venture(models.Model):
    status = models.PositiveSmallIntegerField(
        choices=VENTURE_STATUS_CHOICES,
        default=VENTURE_STATUS_ACTIVE,
        verbose_name=_('status'),
    )

    status_tracker = FieldTracker(fields=['status'])

    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
    )

    logo = models.ImageField(
        max_length=255,
        blank=True,
        help_text='150x150',
        validators=[FileSizeValidator(4000)],
    )

    description_es = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('spanish description'),
    )

    description_en = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('english description'),
    )

    industry_categories = models.ManyToManyField(
        'account.IndustryCategory',
    )

    country = models.ForeignKey(
        'place.Country',
        null=True,
        verbose_name=_('country'),
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        verbose_name=_('state'),
    )

    city = models.ForeignKey(
        'place.City',
        null=True,
        verbose_name=_('city'),
    )

    address = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('address'),
    )

    point = PointField(
        verbose_name=_('location'),
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('contact email'),
    )

    phone_number = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_('contact phone'),
    )

    url = models.URLField(
        blank=True,
        verbose_name=_('webpage'),
    )

    facebook_url = models.URLField(
        blank=True,
        verbose_name=_('Facebook url'),
    )

    twitter_url = models.URLField(
        blank=True,
        verbose_name=_('Twitter url'),
    )

    instagram_url = models.URLField(
        blank=True,
        verbose_name=_('Instagram url'),
    )

    linkedin_url = models.URLField(
        blank=True,
        verbose_name=_('Linkedin url'),
    )

    googleplus_url = models.URLField(
        blank=True,
        verbose_name=_('Google plus url'),
    )

    owner = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name=_('created by'),
    )

    shared_on_twitter = models.BooleanField(
        default=False,
        verbose_name=_('shared on twitter'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField()

    has_new_messages = models.BooleanField(
        default=False,
        verbose_name=_('has new messages'),
    )

    def clean(self):
        if not self.status_tracker.has_changed('status') or not self.id:
            return

        msg = 'Invalid previous status for {0}'
        previous = self.status_tracker.previous('status')

        if (
            self.status == VENTURE_STATUS_INACTIVE and
            previous != VENTURE_STATUS_HIDDEN
        ):
            raise ValidationError({
                'status': msg.format('VENTURE_STATUS_INACTIVE')
            })
        elif (
            self.status == VENTURE_STATUS_HIDDEN and
            previous != VENTURE_STATUS_INACTIVE
        ):
            raise ValidationError({
                'status': msg.format('VENTURE_STATUS_HIDDEN')
            })

    @property
    def is_active(self):
        return self.status == VENTURE_STATUS_ACTIVE

    @property
    def is_inactive(self):
        return self.status == VENTURE_STATUS_INACTIVE

    @property
    def is_hidden(self):
        return self.status == VENTURE_STATUS_HIDDEN

    @property
    def get_logo(self):
        logo = '/static/img/venture_default_logo.svg'
        if self.logo:
            logo = self.logo.url

        return logo

    @property
    def get_score(self):
        user_scores = CompanyScore.objects.filter(company=self)
        total_score = 0

        if user_scores:
            for user_score in user_scores.all():
                total_score += user_score.score

            return total_score / user_scores.count()

        return total_score

    @property
    def get_votes_quantity(self):
        return CompanyScore.objects.filter(company=self).count()

    @property
    def get_active_administrator_ids(self):
        active_memberships = self.administratormembership_set.filter(
            status=ACTIVE_MEMBERSHIP,
        )

        active_administrators = []

        for membership in active_memberships:
            active_administrators.append(membership.admin.id)

        return active_administrators

    def get_absolute_url(self):
        return reverse(
            'venture_detail',
            args=[self.slug],
        )

    def __str__(self):
        return '{0}'.format(self.name)


class CompanyScore(models.Model):
    user = models.ForeignKey(
        'account.User',
        verbose_name=_('usuario'),
    )

    company = models.ForeignKey(
        'entrepreneur.Venture',
        verbose_name=_('company'),
    )

    score = models.FloatField()

    comment = models.TextField(
        verbose_name=_('comment'),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return '{0} - {1} - {2}'.format(
            self.user.get_full_name,
            self.company.name,
            self.score,
        )


class AdministratorMembership(models.Model):
    admin = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name=_('Administrator'),
    )

    venture = models.ForeignKey(
        'entrepreneur.Venture',
        verbose_name=_('company'),
    )

    status = models.PositiveSmallIntegerField(
        choices=MEMBERSHIP_STATUS_CHOICES,
        default=SENT_INVITATION,
    )

    role = models.PositiveSmallIntegerField(
        choices=ADMINISTRATOR_ROLES,
        default=QJANE_ADMIN,
    )

    created_by = models.ForeignKey(
        'account.ProfessionalProfile',
        related_name='membership_owner',
        verbose_name=_('Administrator'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def invitation(self):
        return self.usernotification_set.all().first()

    @property
    def is_active(self):
        return self.status == ACTIVE_MEMBERSHIP

    @property
    def is_rejected(self):
        return self.status == REJECTED_MEMBERSHIP

    def __str__(self):
        return '{0} - {1}'.format(
            self.admin,
            self.venture,
        )


class JobOffer(models.Model):
    status = models.PositiveSmallIntegerField(
        choices=JOB_STATUS_CHOICES,
        default=JOB_STATUS_ACTIVE,
        verbose_name=_('status'),
    )

    status_tracker = FieldTracker(fields=['status'])

    venture = models.ForeignKey(
        Venture,
        verbose_name=_('company'),
    )

    job_type = models.PositiveSmallIntegerField(
        choices=JOB_TYPE_CHOICES,
        default=FREELANCE,
        verbose_name=_('job type'),
    )

    country = models.ForeignKey(
        'place.Country',
        null=True,
        verbose_name=_('country'),
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        verbose_name=_('state'),
    )

    city = models.ForeignKey(
        'place.City',
        null=True,
        verbose_name=_('city'),
    )

    title = models.CharField(
        max_length=80,
        verbose_name=_('title (position)'),
    )

    slug = models.SlugField()

    description = models.TextField(
        verbose_name=_('description'),
    )

    industry_categories = models.ManyToManyField(
        'account.IndustryCategory',
    )

    shared_on_twitter = models.BooleanField(
        default=False,
        verbose_name=_('shared on twitter'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )

    applicants_record = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('applicants register'),
    )

    def clean(self):
        if not self.status_tracker.has_changed('status') or not self.id:
            return

        msg = 'Invalid previous status for {0}'
        previous = self.status_tracker.previous('status')

        if (
            self.status == JOB_STATUS_CLOSED and
            previous != JOB_STATUS_HIDDEN
        ):
            raise ValidationError({
                'status': msg.format('JOB_STATUS_CLOSED')
            })
        elif (
            self.status == JOB_STATUS_HIDDEN and
            previous != JOB_STATUS_CLOSED
        ):
            raise ValidationError({
                'status': msg.format('JOB_STATUS_HIDDEN')
            })

    def get_absolute_url(self):
        return reverse(
            'job_offer_detail',
            args=[self.slug],
        )

    @property
    def is_active(self):
        return self.status == JOB_STATUS_ACTIVE

    @property
    def is_closed(self):
        return self.status == JOB_STATUS_CLOSED

    @property
    def is_hidden(self):
        return self.status == JOB_STATUS_HIDDEN

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('job offer')
        verbose_name_plural = _('job offers')
        ordering = ('-created_at',)


class Applicant(models.Model):
    job_offer = models.ForeignKey(
        'entrepreneur.JobOffer',
        verbose_name=_('job offer'),
    )

    applicant = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name=_('applicant'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )

    class Meta:
        verbose_name = _('applicant')
        verbose_name_plural = _('applicants')
        ordering = ('-created_at',)
