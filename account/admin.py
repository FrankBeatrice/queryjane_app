from django.contrib import admin

# Register your models here.
from account.models import ProfessionalProfile
from account.models import IndustryCategory


class ProfessionalProfileAdmin(admin.ModelAdmin):

    list_display = [
        'user',
    ]


admin.site.register(ProfessionalProfile, ProfessionalProfileAdmin)


class IndustryCategoryAdmin(admin.ModelAdmin):

    list_display = [
        'name_es',
        'name_en',
    ]

    search_fields = [
        'name_es',
        'name_en',
    ]


admin.site.register(IndustryCategory, IndustryCategoryAdmin)
