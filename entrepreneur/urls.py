from django.conf.urls import url

from .views import VentureFormView
from .views import SettingsVentureFormView
from .views import UpdateVentureLogoForm
from .views import ContactVentureFormView
from .views import AjaxContactVentureFormView
from .views import AjaxLocationVentureFormView
from .views import RolesVentureFormView
from .views import JobOffersListView
from .views import JobOfferFormView
from .views import PrivacyVentureFormView
from .views import MembershipLineView
from .views import UpdateVentureDescriptionForm
from .views import VentureCategoryView
from .views import VentureSearch


urlpatterns = [
    url(
        r'^$',
        VentureFormView.as_view(),
        name='venture_form',
    ),
    url(
        r'^ax_venture_autocomplete/$',
        VentureSearch.as_view(),
        name='ax_ventury_autocomplete',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/$',
        SettingsVentureFormView.as_view(),
        name='settings_venture_form',
    ),

    url(
        r'^ax_settings/(?P<slug>[-\w]+)/update_logo/$',
        UpdateVentureLogoForm.as_view(),
        name='update_venture_logo_form',
    ),

    url(
        r'^ax_update_venture_category/(?P<slug>[-\w]+)/$',
        VentureCategoryView.as_view(),
        name='ax_update_venture_category',
    ),

    url(
        r'^ax_settings/(?P<slug>[-\w]+)/update_description/$',
        UpdateVentureDescriptionForm.as_view(),
        name='update_venture_description_form',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/contact/$',
        ContactVentureFormView.as_view(),
        name='contact_venture_form',
    ),

    url(
        r'^ax-update-venture-contact/(?P<pk>\d+)/$',
        AjaxContactVentureFormView.as_view(),
        name='ax_contact_venture_form',
    ),

    url(
        r'^ax-update-venture-location/(?P<pk>\d+)/$',
        AjaxLocationVentureFormView.as_view(),
        name='ax_location_venture_form',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/roles/$',
        RolesVentureFormView.as_view(),
        name='roles_venture_form',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/job_offers/$',
        JobOffersListView.as_view(),
        name='job_offers_list',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/job_offer_form/$',
        JobOfferFormView.as_view(),
        name='job_offer_form',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/privacy/$',
        PrivacyVentureFormView.as_view(),
        name='privacy_venture_form',
    ),

    url(
        r'^get-membership-line/$',
        MembershipLineView.as_view(),
        name='membership_line_url',
    ),
]
