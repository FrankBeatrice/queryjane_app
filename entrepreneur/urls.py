from django.conf.urls import url

from .views.contact_venture_settings import AjaxMediaVentureFormView
from .views.contact_venture_settings import AjaxContactVentureFormView
from .views.contact_venture_settings import AjaxLocationVentureFormView
from .views.contact_venture_settings import ContactVentureFormView
from .views.general_venture_settings import GeneralVentureFormView
from .views.general_venture_settings import UpdateVentureDescriptionForm
from .views.general_venture_settings import UpdateVentureLogoForm
from .views.general_venture_settings import VentureCategoryView
from .views.manage_job_offers import JobOfferFormView
from .views.manage_job_offers import JobOffersListView
from .views.privacy_venture_settings import PrivacyVentureFormView
from .views.roles_venture_settings import MembershipLineView
from .views.roles_venture_settings import RolesVentureFormView
from .views.venture_views import VentureFormView
from .views.venture_views import VentureSearch


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
        r'^general/(?P<slug>[-\w]+)/$',
        GeneralVentureFormView.as_view(),
        name='general_venture_form',
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
        r'^ax-update-venture-media/(?P<pk>\d+)/$',
        AjaxMediaVentureFormView.as_view(),
        name='ax_media_venture_form',
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
