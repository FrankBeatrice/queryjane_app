from django.conf.urls import url
from django.views.generic import TemplateView

from .views import AdminDashboardView
from .views import TwitterShareVentureView

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
]
