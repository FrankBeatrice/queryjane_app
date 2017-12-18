from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone

from .data import NOTIFICATION_TYPE_CHOICES
from .data import NEW_ENTREPRENEUR_ADMIN


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            is_active=is_active,
        )
        user.first_name = 'Jane'
        user.last_name = 'QueryUser'
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    first_name = models.CharField(
        verbose_name='nombres',
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(3),
        ],
        error_messages={
            'min_length':
                'El campo "Nombre" debe tener al menos %(limit_value)d '
                'caracteres (actualmente tiene %(show_value)d).'
        }
    )

    last_name = models.CharField(
        verbose_name='last name',
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(3),
        ],
        error_messages={
            'min_length':
                'El campo "Apellidos" debe tener al menos %(limit_value)d '
                'caracteres (actualmente tiene %(show_value)d).'
        }
    )

    email = models.EmailField(
        verbose_name='email',
        unique=True,
        blank=False,
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Indica si el usuario puede entrar en este sitio '
                  'de administración.',
    )

    is_active = models.BooleanField(
        'Activo',
        default=True,
        help_text='Indica si el usuario puede ser tratado como activo. '
                  'Desmarque esta opción en lugar de borrar la cuenta.',
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
        verbose_name='dirección',
        max_length=80,
        null=True,
        blank=True,
    )

    date_joined = models.DateTimeField(
        verbose_name='fecha de creación',
        default=timezone.now,
    )

    objects = UserManager()

    @property
    def get_country(self):
        country = None

        if self.country:
            country = self.country.country

        return country

    @property
    def get_full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    @property
    def get_short_name(self):
        return self.first_name if self.first_name else self.email.split('@')[0]

    def __str__(self):
        return self.get_full_name

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ('email',)


class ProfessionalProfile(models.Model):
    BOOL_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )

    user = models.OneToOneField(
        'account.User',
        verbose_name='Cuenta de usuario',
    )

    description = models.TextField(
        blank=True,
        verbose_name='description',
    )

    phone_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Phone number',
    )

    industry_categories = models.ManyToManyField(
        'account.IndustryCategory',
        blank=True,
    )

    apply_jobs = models.BooleanField(
        default=True,
        choices=BOOL_CHOICES,
        verbose_name='¿Deseas aplicar a ofertas de trabajo publicadas en tus sectores de interés?',
    )

    email_jobs_notifications = models.BooleanField(
        default=True,
        verbose_name='Recibir notificaciones de ofertas e trabajo via e-mail.',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField()

    def __str__(self):
        return '{0}'.format(self.user)

    @property
    def get_print(self):
        return self.user.get_full_name


class IndustryCategory(models.Model):
    name_es = models.CharField(
        max_length=50,
        verbose_name='spanish name',
    )

    description_es = models.TextField(
        blank=True,
        null=True,
        verbose_name='spanish description',
    )

    name_en = models.CharField(
        max_length=50,
        verbose_name='english name',
    )

    description_en = models.TextField(
        blank=True,
        null=True,
        verbose_name='english description',
    )

    class Meta:
        ordering = ('name_en',)

    def __str__(self):
        return '{0}'.format(self.name_en)


class UserNotification(models.Model):
    notification_type = models.PositiveSmallIntegerField(
        choices=NOTIFICATION_TYPE_CHOICES,
    )

    description = models.TextField(
        verbose_name='description',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    was_seen = models.BooleanField(
        default=False,
    )

    noty_to = models.ForeignKey(
        'account.User',
        verbose_name='Notificar a',
    )

    venture_from = models.ForeignKey(
        'entrepreneur.Venture',
        verbose_name='from venture',
        null=True,
    )

    membership = models.ForeignKey(
        'entrepreneur.AdministratorMembership',
        verbose_name='membership invitation',
        null=True,
    )

    created_by = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name='creada por',
        related_name='creator',
    )

    answered = models.BooleanField(
        default=False,
    )

    @property
    def is_new_entrepreneur_admin(self):
        return self.notification_type == NEW_ENTREPRENEUR_ADMIN

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        if self.is_new_entrepreneur_admin:
            label = 'invitation from {}'.format(
                self.created_by,
            )
        return label
