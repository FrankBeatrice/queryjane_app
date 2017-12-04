from django.contrib import admin

# Register your models here.
from .models import Venture


class VentureAdmin(admin.ModelAdmin):

    list_display = [
        'name',
    ]


admin.site.register(Venture, VentureAdmin)
