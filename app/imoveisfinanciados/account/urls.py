from django.urls import path,re_path
from django.contrib.auth import views as auth_views

from imoveisfinanciados.account import views as auser_views


app_name = 'account'
urlpatterns = [
    re_path('login/$',
        auser_views.login,
        {'template_name': 'account/login.html'},
        name='auth_login'
        ),
    re_path('logout/$', auser_views.logout, name='auth_logout'),
    re_path('register/$',
        auser_views.register,
        {'template_name': 'account/register.html'},
        name="auth_register"
        ),
    re_path('register/successful/$',
        auser_views.registration_successful,
        {"template_name": "account/registration_successful.html"},
        name="registration_successful"
        ),
    re_path('password/change/$',
        auth_views.PasswordChangeView.as_view(),
        {
            'template_name': 'account/change-password.html',
            'post_change_redirect': 'accounts:auth_password_change_done'
        },
        name='auth_password_change'
        ),
    re_path('password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(),
        {
            'template_name': 'account/change-password-done.html',
        },
        name='auth_password_change_done'
        ),
    re_path('profile/$', auser_views.ProfileUpdateView.as_view(),
        name='auth_profile'),
    # path('manage/', auser_views.manage.as_view(), name='auth_manage'),
    re_path('password/reset/$',
        auth_views.PasswordResetView.as_view(),
        {
            'template_name': 'account/reset-password.html',
            'post_reset_redirect': 'accounts:auth_password_reset_done',
            'email_template_name': 'account/password-reset-email.html',
        },
        name='auth_password_reset'
        ),
    re_path('password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(),
        {
            'template_name': 'account/password-reset-confirm.html',
            'post_reset_redirect': 'accounts:auth_password_reset_complete',
        },
        name='auth_password_reset_confirm'
        ),
    re_path('password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        {
            'template_name': 'account/password-reset-complete.html',
        },
        name='auth_password_reset_complete'
        ),
    re_path('password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        {
            'template_name': 'account/password-reset-sent.html',
        },
        name='auth_password_reset_done'
        ),
]
