from django.db import models
from django.utils.text import slugify


class CorporativeInfo(models.Model):
    title_sp = models.CharField(
        max_length=50,
        verbose_name='título',
    )

    title_en = models.CharField(
        max_length=50,
        verbose_name='title',
    )

    description_sp = models.TextField(
        verbose_name='descripción',
    )

    description_en = models.TextField(
        verbose_name='description',
    )

    slug = models.SlugField()

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'ítem informativo'
        verbose_name_plural = 'ítems informativos'
        ordering = ('id',)
