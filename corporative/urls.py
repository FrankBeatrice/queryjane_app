from django.conf.urls import url
from django.views.generic import TemplateView

from .views import AdminDashboardView
from .views import TwitterShareVentureView
from .views import TwitterShareJobView
from .views import HideVentureView
from .views import ActivateVentureView

urlpatterns = [
    url(
        r'^user-agreement/$',
        TemplateView.as_view(template_name='corporative/user_agreement.html'),
        name='user_agreement',
    ),

    url(
        r'^privacy-policy/$',
        TemplateView.as_view(template_name='corporative/privacy_policy.html'),
        name='privacy_policy',
    ),

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
]
