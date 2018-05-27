from django.conf.urls import url

from .views import ActivateJobOfferView
from .views import ActivateVentureView
from .views import AdminDashboardView
from .views import HideJobOfferView
from .views import HideVentureView
from .views import LegalItemView
from .views import LegalItemFormView
from .views import TwitterShareJobView
from .views import TwitterShareVentureView

urlpatterns = [
    url(
        r'^admin_dashboard/$',
        AdminDashboardView.as_view(),
        name='admin_dashboard',
    ),

    url(
        r'^ax-twitter-share/(?P<slug>[-\w]+)/venture/$',
        TwitterShareVentureView.as_view(),
        name='ax_twitter_share_venture',
    ),

    url(
        r'^ax-twitter-share/(?P<slug>[-\w]+)/job/$',
        TwitterShareJobView.as_view(),
        name='ax_twitter_share_job',
    ),

    url(
        r'^ax-hide/(?P<slug>[-\w]+)/venture/$',
        HideVentureView.as_view(),
        name='ax_hide_venture',
    ),

    url(
        r'^ax-activate/(?P<slug>[-\w]+)/venture/$',
        ActivateVentureView.as_view(),
        name='ax_activate_venture',
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
        r'^ax-twitter-share/(?P<slug>[-\w]+)/venture/$',
        TwitterShareVentureView.as_view(),
        name='ax_twitter_share_venture',
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
