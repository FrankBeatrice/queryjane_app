from django.contrib import admin


from corporative.models import CorporativeInfo


@admin.register(CorporativeInfo)
class CorporativeInfoAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    list_display = (
        'title_sp',
        'title_en',
    )

    readonly_fields = (
        'title_sp',
        'title_en',
        'slug',
    )

    fieldsets = (
        ('Ítem', {
            'fields': (
                'title_sp',
                'title_en',
                'slug',
            ),
        }),
        ('Descripción', {
            'fields': (
                'description_sp',
                'description_en',
            ),
        }),
    )

    class Media:
        css = {
            'all': (
                'libs/redactor/redactor.min.css',
                'css/admin.css',
            )
        }
        js = (
            '//code.jquery.com/jquery-latest.min.js',
            'js/admin.js',
        )
