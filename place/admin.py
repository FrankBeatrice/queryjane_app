from django.contrib import admin

# Register your models here.
from .models import City
from .models import State
from .models import Country


class CityAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'state',
    ]

admin.site.register(City, CityAdmin)


class StateAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'country',
    ]

admin.site.register(State, StateAdmin)


class CountryAdmin(admin.ModelAdmin):

    list_display = [
        'country',
    ]

admin.site.register(Country, CountryAdmin)
