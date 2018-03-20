from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from .views import ajax_login_form
from .views import ContactFormView
from .views import HomeView
from .views import DashboardView
from .views import JobOfferApplyView
from .views import JobOfferDetail
from .views import JobsList
from .views import ProfessionalDetail
from .views import user_logout
from .views import VentureDetail
from .views import VentureList
from account.forms import UserPasswordResetForm

admin.site.site_title = 'QueryJane'
admin.site.site_header = 'QueryJane - Administrador'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    url(
        r'^$',
        HomeView.as_view(),
        name='home',
    ),

    url(
        r'^dashbaord/$',
        DashboardView.as_view(),
        name='dashboard',
    ),

    url(
        r'^companies/$',
        VentureList.as_view(),
        name='venture_list',
    ),

    url(
        r'^jobs/$',
        JobsList.as_view(),
        name='jobs_list',
    ),

    url(
        r'^jobs/(?P<slug>[-\w]+)/$',
        JobOfferDetail.as_view(),
        name='job_offer_detail',
    ),

    url(
        r'^jobs/(?P<slug>[-\w]+)/apply/$',
        JobOfferApplyView.as_view(),
        name='job_offer_apply',
    ),

    url(
        r'^contact_form/$',
        ContactFormView.as_view(),
        name='contact_form',
    ),

    url(
        r'^contact_form_success/$',
        TemplateView.as_view(template_name='corporative/contact_form_success.html'),
        name='contact_form_success',
    ),

    url(
        r'^password/recovery/$',
        auth_views.PasswordResetView.as_view(
            template_name='account/auth/password_reset_form.html',
            form_class=UserPasswordResetForm,
            html_email_template_name='account/auth/password_reset_email.html',
        ),
        name='password_reset',
    ),

    url(
        r'^password/recovery/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/auth/password_reset_done.html',
        ),
        name='password_reset_done',
    ),

    url(
        r'^password/recovery/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('auth_login'),
            post_reset_login=True,
            template_name='account/auth/password_reset_confirm.html',
            post_reset_login_backend=(
                'django.contrib.auth.backends.AllowAllUsersModelBackend'
            ),
        ),
        name='password_reset_confirm',
    ),

    # Login Form
    url(
        r'^general-login-form/$',
        ajax_login_form,
        name='ajax_login_form',
    ),

    url(
        r'^login/$',
        auth_views.login,
        {
            'template_name': 'account/auth/login.html',
            'redirect_authenticated_user': True,
        },
        name='auth_login',
    ),

    url(
        r'^logout/$',
        user_logout,
        name='user_logout',
    ),

    url(
        r'^corporative/',
        include(
            'corporative.urls',
            namespace='corporative',
        )
    ),
    url(r'^account/', include('account.urls', namespace='account')),
    url(
        r'^entrepreneur/',
        include(
            'entrepreneur.urls',
            namespace='entrepreneur',
        )
    ),
    url(r'^place/', include('place.urls', namespace='place')),

    url(
        r'^(?P<slug>[-\w]+)/$',
        VentureDetail.as_view(),
        name='venture_detail',
    ),
    url(
        r'^profile/(?P<slug>[-\w]+)/$',
        ProfessionalDetail.as_view(),
        name='professional_detail',
    ),
)
