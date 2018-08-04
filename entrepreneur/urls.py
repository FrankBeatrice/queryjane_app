from django.conf.urls import url

from .views.contact_venture_settings import AjaxContactVentureFormView
from .views.contact_venture_settings import AjaxLocationVentureFormView
from .views.contact_venture_settings import AjaxMediaVentureFormView
from .views.contact_venture_settings import ContactCompanyFormView
from .views.general_venture_settings import GeneralCompanyFormView
from .views.general_venture_settings import UpdateVentureDescriptionForm
from .views.general_venture_settings import UpdateCompanyLogoForm
from .views.general_venture_settings import CompanyCategoryView
from .views.manage_job_offers import JobOfferCloseView
from .views.manage_job_offers import JobOfferFormView
from .views.manage_job_offers import JobOffersListView
from .views.manage_job_offers import JobOfferUpdateView
from .views.messages import MessagesView
from .views.privacy_venture_settings import PrivacyVentureFormView
from .views.roles_venture_settings import MembershipLineView
from .views.roles_venture_settings import RolesCompanyFormView
from .views.venture_views import VentureFormView
from .views.venture_views import CompanySearch


urlpatterns = [
    url(
        r'^$',
        VentureFormView.as_view(),
        name='venture_form',
    ),
    url(
        r'^ax_company_autocomplete/$',
        CompanySearch.as_view(),
        name='ax_company_autocomplete',
    ),

    url(
        r'^general/(?P<slug>[-\w]+)/$',
        GeneralCompanyFormView.as_view(),
        name='general_venture_form',
    ),

    url(
        r'^ax_settings/(?P<slug>[-\w]+)/update_logo/$',
        UpdateCompanyLogoForm.as_view(),
        name='update_company_logo_form',
    ),

    url(
        r'^ax_update_company_category/(?P<slug>[-\w]+)/$',
        CompanyCategoryView.as_view(),
        name='ax_update_company_category',
    ),

    url(
        r'^ax_settings/(?P<slug>[-\w]+)/update_description/$',
        UpdateVentureDescriptionForm.as_view(),
        name='update_company_description_form',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/contact/$',
        ContactCompanyFormView.as_view(),
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
        RolesCompanyFormView.as_view(),
        name='roles_venture_form',
    ),

    url(
        r'^settings/(?P<slug>[-\w]+)/messages/$',
        MessagesView.as_view(),
        name='messages_adim',
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
        r'^settings/(?P<slug>[-\w]+)/job_offer_update/$',
        JobOfferUpdateView.as_view(),
        name='job_offer_update',
    ),

    url(
        r'^ax-settings/(?P<slug>[-\w]+)/job_offer_close/$',
        JobOfferCloseView.as_view(),
        name='job_offer_close',
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
