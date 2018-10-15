from django.conf.urls import url

from .views import ActivateJobOfferView
from .views import ActivateCompanyView
from .views import AdminDashboardView
from .views import HideJobOfferView
from .views import HideCompanyView
from .views import LegalItemView
from .views import LegalItemFormView
from .views import TwitterShareJobView
from .views import TwitterShareCompanyView
from .views import LegalItemAgreeView
from .views import CityBulkFormView

urlpatterns = [
    url(
        r'^admin_dashboard/$',
        AdminDashboardView.as_view(),
        name='admin_dashboard',
    ),

    url(
        r'^ax-twitter-share/(?P<slug>[-\w]+)/venture/$',
        TwitterShareCompanyView.as_view(),
        name='ax_twitter_share_company',
    ),

    url(
        r'^ax-twitter-share/(?P<slug>[-\w]+)/job/$',
        TwitterShareJobView.as_view(),
        name='ax_twitter_share_job',
    ),

    url(
        r'^ax-hide/(?P<slug>[-\w]+)/venture/$',
        HideCompanyView.as_view(),
        name='ax_hide_company',
    ),

    url(
        r'^ax-activate/(?P<slug>[-\w]+)/venture/$',
        ActivateCompanyView.as_view(),
        name='ax_activate_company',
    ),

    url(
        r'^ax-hide/(?P<slug>[-\w]+)/job_offer/$',
        HideJobOfferView.as_view(),
        name='ax_hide_job_offer',
    ),

    url(
        r'^ax-activate/(?P<slug>[-\w]+)/job_offer/$',
        ActivateJobOfferView.as_view(),
        name='ax_activate_job_offer',
    ),

    url(
        r'^legal_item_agree/(?P<slug>[-\w]+)/$',
        LegalItemAgreeView.as_view(),
        name='legal_item_agree',
    ),

    url(
        r'^city-bulk-form/$',
        CityBulkFormView.as_view(),
        name='city_bulk_form',
    ),

    url(
        r'^(?P<slug>[-\w]+)/update/$',
        LegalItemFormView.as_view(),
        name='legal_item_form',
    ),
    url(
        r'^(?P<slug>[-\w]+)/',
        LegalItemView.as_view(),
        name='legal_item',
    ),
]
