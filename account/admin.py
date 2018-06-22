from django.contrib import admin

# Register your models here.
from account.models import IndustryCategory


class IndustryCategoryAdmin(admin.ModelAdmin):
    """Activate Django default administration for
    industry categories. Users with platform administration
    permission can manage intrustry categories.
    """
    list_display = [
        'name_es',
        'name_en',
    ]

    search_fields = [
        'name_es',
        'name_en',
    ]


admin.site.register(IndustryCategory, IndustryCategoryAdmin)
