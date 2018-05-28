from django.db import models
from django.utils.translation import ugettext as _


class LegalItem(models.Model):
    sp_title = models.CharField(
        max_length=50,
        verbose_name=_('Spanish title'),
    )

    en_title = models.CharField(
        max_length=50,
        verbose_name=_('English title'),
    )

    sp_description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Spanish description'),
    )

    en_description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('English description'),
    )

    slug = models.SlugField()

    updated_at = models.DateTimeField()

    def __str__(self):
        return '{0}'.format(self.en_title)

    class Meta:
        verbose_name = _('Legal item')
        verbose_name_plural = _('Legal items')
        ordering = ('-updated_at',)
