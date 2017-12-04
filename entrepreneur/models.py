from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.gis.db.models import PointField
from app.validators import FileSizeValidator

from .data import ADMINISTRATOR_ROLES
from .data import QJANE_ADMIN
from .data import MEMBERSHIP_STATUS_CHOICES
from .data import REJECTED_MEMBERSHIP
from .data import SENT_INVITATION
from .data import ACTIVE_MEMBERSHIP


class Venture(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='nombre',
    )

    logo = models.ImageField(
        upload_to='uploads/ventures/',
        max_length=255,
        blank=True,
        help_text='150x150',
        validators=[FileSizeValidator(4000)],
    )

    description_es = models.TextField(
        verbose_name='descripción',
    )

    description_en = models.TextField(
        verbose_name='description',
    )

    industry_categories = models.ManyToManyField(
        'account.IndustryCategory',
    )

    country = models.ForeignKey(
        'place.Country',
        null=True,
        verbose_name='país',
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
        verbose_name='dirección',
    )

    point = PointField(
        verbose_name='posición',
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='correo electrónico de contacto',
    )

    phone_number = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='teléfono de contacto',
    )

    url = models.URLField(
        blank=True,
        verbose_name='Página web',
    )

    facebook_url = models.URLField(
        blank=True,
        verbose_name='Página de Facebook',
    )

    twitter_url = models.URLField(
        blank=True,
        verbose_name='Página de Twitter',
    )

    instagram_url = models.URLField(
        blank=True,
        verbose_name='Página de Instagram',
    )

    linkedin_url = models.URLField(
        blank=True,
        verbose_name='Página de Linkedin',
    )

    googleplus_url = models.URLField(
        blank=True,
        verbose_name='Página de Google +',
    )

    is_active = models.BooleanField(
        default=True,
    )

    owner = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name='Creada por',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField()

    @property
    def get_logo(self):
        logo = '/static/img/venture_default_logo.png'
        if self.logo:
            logo = self.logo.url

        return logo

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
        verbose_name='Administrador',
    )

    venture = models.ForeignKey(
        'entrepreneur.Venture',
        verbose_name='Empresa',
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
        verbose_name='Administrador',
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
