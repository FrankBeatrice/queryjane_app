from django.conf import settings

from corporative.permissions import AdminPermissions


def facebook_app_id(request):
    return {'FACEBOOK_APP_ID': settings.SOCIAL_AUTH_FACEBOOK_KEY}


def permissions(request):
    user = request.user
    if user.is_anonymous():
        return {}

    perms = {}

    perms['manage_admin_views'] = AdminPermissions.can_manage_admin_views(
        user=user,
    )

    data = {
        'permission_app': perms,
    }

    return data
