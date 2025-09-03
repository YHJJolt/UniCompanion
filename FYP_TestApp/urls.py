from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    # all usual urls
    path('', signUp_view,           name='signup'),
    path('accounts/login/', logout_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view,        name='home'),
    path('home_create_post/', home_createPost_view, name='home_create_post'),
    path('calendar/', events_view,    name='calendar'),
    path('saved/', saved_view,      name='saved'),
    path('profile/', profile_view,  name='profile'),
    path('companion/', companion_view, name='companion'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('app_settings/', app_settings_view, name='app_settings'),
    path('check_password/', app_settings_checkPass_view, name='check_password'),
    path('edit_password/', app_settings_editPass_view, name='edit_password'),
    path('delete_acc/', app_settings_deleteAcc_view, name='delete_acc'),
    path('help_center/', help_center_view, name='help_center'),
    path('indivPost/', indivPost_view, name='indivPost'),
    path('notification/', notification_view, name='notification'),
    path('banned/', banned_view, name='banned'),
    path('add_appeal/', addAppeal_view, name='add_appeal'),

    # admin
    path('admin_dashboard/', adminDashboard_view, name='admin_dashboard'),
    path('admin_reported_content/', adminReportedContent_view, name='admin_reported'),
    path('admin_reported_delete/', adminReportedContentDelete_view, name='admin_reported_delete'),
    path('admin_reported_dismiss/', adminReportedContentDismiss_view, name='admin_reported_dismiss'),
    path('admin_flair/', adminFlair_view, name='admin_flair'),
    path('admin_add_flair/', adminAddFlair_view, name='admin_add_flair'),
    path('admin_del_flair/', adminDelFlair_view, name='admin_del_flair'),
    path('admin_faq/', adminEditFAQ_view, name='admin_faq'),
    path('admin_faq_add', adminEditFAQAdd_view, name='admin_faq_add'),
    path('admin_faq_delete', adminEditFAQDelete_view, name='admin_faq_delete'),
    path('admin_appeal/',adminAppeal_view, name='admin_appeal' ),
    path('admin_appeal_approve/',adminAppealApprove_view, name='admin_appeal_approve' ),
    path('admin_appeal_deny/',adminAppealDeny_view, name='admin_appeal_deny' ),

    # reporting
    path('report_post/', report_post_view, name='report_post'),
    path('report_comment/', report_comment_view, name='report_comment'),
    path('report_user/', report_user_view, name='report_user'),

    # creating account
    path('check-email/', check_email_exists, name='check_email'),
    path('check-login/' , login_view, name='login'),

    # calendar events
    path('add_event/' , event_add_view, name='add_event'),
    path('edit_event/' , event_edit_view, name='edit_event'),
    path('delete_event/' , event_delete_view, name='delete_event'),

    # profile
    path('profile_add/', profile_add_view, name='profile_add'),
    path('profile_edit/', profile_edit_view, name='profile_edit'),

    # post
    path('like_post/', post_like_view, name='like_post'),
    path('indivPost_addComment_view/', indivPost_addComment_view, name='indivPost_addComment'),

    # comments
    path('like_comment/', comment_like_view, name='like_comment'),

    # notification
    path('mark_notification/', mark_notification_view, name='mark_notification'),

    # search
    path('search/', search_view, name='search'),
]
