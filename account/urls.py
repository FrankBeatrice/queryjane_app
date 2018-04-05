from django.conf.urls import url

from account.views.address_book import AddressBookView
from account.views.address_book import AddUserToAddressBookView
from account.views.address_book import AddCompanyToAddressBookView
from account.views.address_book import RemoveUserFromAddressBookView
from account.views.address_book import RemoveCompanyToAddressBookView
from account.views.messages import InboxView
from account.views.messages import LoadMessageModal
from account.views.messages import LoadConversationView
from account.views.messages import UserMessageFormView
from account.views.notifications import AdminNotificationAcceptView
from account.views.notifications import AdminNotificationRejectView
from account.views.notifications import AdminNotificationResendView
from account.views.notifications import LoadNotificationModal
from account.views.notifications import NotificationsView
from account.views.profile import NewUserLandingView
from account.views.profile import ProfessionalProfileCategoryView
from account.views.profile import ProfileSearch
from account.views.profile import SignUpFormView
from account.views.profile import UpdateProfileAvatarForm
from account.views.profile import UpdateProfileDescriptionForm
from account.views.profile import UpdateProfileFormView
from account.views.profile import EmailNotificationsUpdateView

urlpatterns = [
    url(
        r'^$',
        SignUpFormView.as_view(),
        name='signup_form_submit',
    ),

    # API Userprofile
    url(
        r'^profile-search/$',
        ProfileSearch.as_view(),
        name='profile-search',
    ),

    url(
        r'^landing/$',
        NewUserLandingView.as_view(),
        name='signup_landing',
    ),

    url(
        r'^update/$',
        UpdateProfileFormView.as_view(),
        name='profile_update',
    ),

    url(
        r'^address-book/$',
        AddressBookView.as_view(),
        name='address_book',
    ),

    url(
        r'^ax_update_professional_profile_category/$',
        ProfessionalProfileCategoryView.as_view(),
        name='ax_update_professional_profile_category',
    ),

    url(
        r'^ax_account/update_description/$',
        UpdateProfileDescriptionForm.as_view(),
        name='update_profile_description_form',
    ),

    url(
        r'^ax-post-notification-load/(?P<pk>\d+)/$',
        LoadNotificationModal.as_view(),
        name='ajax_post_notification_load',
    ),

    url(
        r'^admin_notification_accept/(?P<pk>\d+)/$',
        AdminNotificationAcceptView.as_view(),
        name='admin_notification_accept',
    ),

    url(
        r'^admin_notification_reject/(?P<pk>\d+)/$',
        AdminNotificationRejectView.as_view(),
        name='admin_notification_reject',
    ),

    url(
        r'^ax_admin_notification_resend/(?P<pk>\d+)/$',
        AdminNotificationResendView.as_view(),
        name='admin_notification_resend',
    ),

    url(
        r'^ax_send_user_mesasge/$',
        UserMessageFormView.as_view(),
        name='send_user_mesasge',
    ),

    url(
        r'^ax-post-message-load/(?P<pk>\d+)/$',
        LoadMessageModal.as_view(),
        name='ajax_post_message_load',
    ),

    url(
        r'^ax-post-conversation-load/(?P<pk>\d+)/$',
        LoadConversationView.as_view(),
        name='ajax_post_conversation_load',
    ),

    url(
        r'^inbox/$',
        InboxView.as_view(),
        name='inbox_view',
    ),

    url(
        r'^notifications/$',
        NotificationsView.as_view(),
        name='notifications_view',
    ),

    url(
        r'^ax_profile_avatar/$',
        UpdateProfileAvatarForm.as_view(),
        name='update_profile_avatar_form',
    ),

    url(
        r'^ax_email_notification_update/$',
        EmailNotificationsUpdateView.as_view(),
        name='ax_email_notification_update',
    ),

    url(
        r'^ax_add_user_to_address_book/(?P<pk>\d+)/$',
        AddUserToAddressBookView.as_view(),
        name='ajax_add_user_to_address_book',
    ),

    url(
        r'^ax_remove_user_from_address_book/(?P<pk>\d+)/$',
        RemoveUserFromAddressBookView.as_view(),
        name='ajax_remove_user_from_address_book',
    ),

    url(
        r'^ax_add_company_to_address_book/(?P<pk>\d+)/$',
        AddCompanyToAddressBookView.as_view(),
        name='ajax_add_company_to_address_book',
    ),

    url(
        r'^ax_remove_company_to_address_book/(?P<pk>\d+)/$',
        RemoveCompanyToAddressBookView.as_view(),
        name='ajax_remove_company_from_address_book',
    ),
]
