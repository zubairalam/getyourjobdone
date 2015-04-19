from django.conf.urls import patterns, url

from .views import DashboardView, LoginView, LogoutView, RegistrationView, RegistrationFailure, RegistrationSuccess, \
    RegistrationConfirmation, ResendConfirmationLink, SendPasswordResetLink, ResetPassword, ResetPasswordSuccess

urlpatterns = patterns('',
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^logout/$', LogoutView.as_view(), name='logout'),
                       url(r'^signup/$', RegistrationView.as_view(), name='registration'),
                       url(r'^signup/success/$', RegistrationSuccess.as_view(), name='registration_success'),
                       url(r'^signup/failure/$', RegistrationFailure.as_view(), name='registration_failure'),
                       url(r'^signup/confirmation/', RegistrationConfirmation.as_view(), name='registration_confirmation'),
                       url(r'^reset_password/success/$', ResetPasswordSuccess.as_view(), name='resetpw_success'),
                       url(r'^reset_password/', ResetPassword.as_view(), name='reset_password'),
                       url(r'^send_resetpw_link/$', SendPasswordResetLink.as_view(), name='send_resetpw_link'),
                       url(r'^signup/resend_confirmation/', ResendConfirmationLink.as_view(),
                       name='resend_confirmation_link'),
                       url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
)
