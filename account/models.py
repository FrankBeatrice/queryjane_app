from __future__ import unicode_literals

from django.utils.text import slugify
from django.utils.crypto import get_random_string
from app.validators import FileSizeValidator

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone

from .data import NOTIFICATION_TYPE_CHOICES
from .data import NEW_ENTREPRENEUR_ADMIN
from .data import NEW_JOB_OFFER
from entrepreneur.models import Venture


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_active=True,
    ):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            is_active=is_active,
        )

        if not first_name:
            first_name = 'Query'
        if not last_name:
            last_name = 'Jane'

        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)

        slug = slugify(
            '{0}{1}'.format(
                first_name,
                last_name,
            )
        )

        if (
            Venture.objects.filter(slug=slug) or
            ProfessionalProfile.objects.filter(slug=slug)
        ):
            random_string = get_random_string(length=6)
            slug = '{0}-{1}'.format(
                slug,
                random_string.lower(),
            )

        ProfessionalProfile.objects.create(
            user=user,
            slug=slug,
        )

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

    avatar = models.ImageField(
        verbose_name='profile image',
        max_length=255,
        blank=True,
        validators=[FileSizeValidator(4000)],
    )

    first_name = models.CharField(
        verbose_name='name',
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
    def get_avatar(self):
        avatar = '/static/img/profile_default_avatar.png'
        if self.avatar:
            avatar = self.avatar.url

        return avatar

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

    description_en = models.TextField(
        blank=True,
        verbose_name='description',
    )

    description_es = models.TextField(
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
        verbose_name='Notify to',
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

    job_offer = models.ForeignKey(
        'entrepreneur.JobOffer',
        verbose_name='related job offer',
        null=True,
    )

    created_by = models.ForeignKey(
        'account.ProfessionalProfile',
        verbose_name='created by',
        related_name='creator',
    )

    answered = models.BooleanField(
        default=False,
    )

    @property
    def is_new_entrepreneur_admin(self):
        return self.notification_type == NEW_ENTREPRENEUR_ADMIN

    @property
    def is_interest_job_offer(self):
        return self.notification_type == NEW_JOB_OFFER

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.description


class UserMessage(models.Model):
    user_from = models.ForeignKey(
        'account.User',
        verbose_name='from',
        related_name='user_from',
    )

    user_to = models.ForeignKey(
        'account.User',
        verbose_name='to',
        related_name='user_to',
    )

    message = models.TextField(
        verbose_name='message',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    unread = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'message from {0}'.format(
            self.user_from.get_full_name,
        )
