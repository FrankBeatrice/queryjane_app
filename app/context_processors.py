from django.conf import settings


def facebook_app_id(request):
    return {'FACEBOOK_APP_ID': settings.SOCIAL_AUTH_FACEBOOK_KEY}
