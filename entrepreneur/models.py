from app.validators import FileSizeValidator
from django.contrib.gis.db.models import PointField
from django.core.urlresolvers import reverse
from django.db import models

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
        verbose_name='status',
    )

    name = models.CharField(
        max_length=50,
        verbose_name='name',
    )

    logo = models.ImageField(
        max_length=255,
        blank=True,
        help_text='150x150',
        validators=[FileSizeValidator(4000)],
    )

    description_es = models.TextField(
        verbose_name='spanish description',
    )

    description_en = models.TextField(
        verbose_name='english description',
    )

    industry_categories = models.ManyToManyField(
        'account.IndustryCategory',
    )

    country = models.ForeignKey(
        'place.Country',
        null=True,
        verbose_name='country',
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        verbose_name='state',
    )

    city = models.ForeignKey(
        'place.City',
        null=True,
        verbose_name='city',
    )

    address = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='address',
    )

    point = PointField(
        verbose_name='location',
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='contact email',
    )

    phone_number = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='contact phone',
    )

    url = models.URLField(
        blank=True,
        verbose_name='webpage',
    )

    facebook_url = models.URLField(
        blank=True,
        verbose_name='Facebook url',
    )

    twitter_url = models.URLField(
        blank=True,
        verbose_name='Twitter url',
    )

    instagram_url = models.URLField(
        blank=True,
        verbose_name='Instagram url',
    )

    linkedin_url = models.URLField(
        blank=True,
        verbose_name='Linkedin url',
    )

    googleplus_url = models.URLField(
        blank=True,
        verbose_name='Google plus url',
    )

    owner = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name='created by',
    )

    shared_on_twitter = models.BooleanField(
        default=False,
        verbose_name='shared on twitter',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField()

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


class AdministratorMembership(models.Model):
    admin = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name='Administrator',
    )

    venture = models.ForeignKey(
        'entrepreneur.Venture',
        verbose_name='company',
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
        verbose_name='Administrator',
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
        verbose_name='status',
    )

    venture = models.ForeignKey(
        Venture,
        verbose_name='company',
    )

    job_type = models.PositiveSmallIntegerField(
        choices=JOB_TYPE_CHOICES,
        default=FREELANCE,
        verbose_name='job type',
    )

    country = models.ForeignKey(
        'place.Country',
        null=True,
        verbose_name='country',
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        verbose_name='state',
    )

    city = models.ForeignKey(
        'place.City',
        null=True,
        verbose_name='city',
    )

    title = models.CharField(
        max_length=80,
        verbose_name='title (position)',
    )

    slug = models.SlugField()

    description = models.TextField(
        verbose_name='description',
    )

    industry_categories = models.ManyToManyField(
        'account.IndustryCategory',
    )

    shared_on_twitter = models.BooleanField(
        default=False,
        verbose_name='shared on twitter',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created at',
    )

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
        verbose_name = 'job offer'
        verbose_name_plural = 'job offers'
        ordering = ('-created_at',)


class Applicant(models.Model):
    job_offer = models.ForeignKey(
        'entrepreneur.JobOffer',
        verbose_name='job offer',
    )

    applicant = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name='applicant',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created at',
    )

    class Meta:
        verbose_name = 'applicant'
        verbose_name_plural = 'applicants'
        ordering = ('-created_at',)
