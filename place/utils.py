import pygeoip

from place.models import Country


def get_user_country(META):
    x_forwarded_for = META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = META.get('REMOTE_ADDR')

    if not ip:
        return None

    gi = pygeoip.GeoIP('app/static/GeoIP.dat')
    country_code = gi.country_code_by_addr('190.252.158.138')
    country_name = gi.country_name_by_addr('190.252.158.138')
    # country_code = gi.country_code_by_addr(ip)
    # country_name = gi.country_name_by_addr(ip)

    country_instance = None

    if country_code:
        country_instance = Country.objects.get_or_create(
            country=country_code,
            name=country_name,
        )[0]

    return country_instance
