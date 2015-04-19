from django.conf.urls import patterns, url

from .views import AboutPageView, ContactPageView, HelpPageView, HomePageView, TermsPageView, PrivacyPageView

urlpatterns = patterns('',
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^about/$', AboutPageView.as_view(), name='about'),
                       url(r'^contact/$', ContactPageView.as_view(), name='contact'),
                       url(r'^help/$', HelpPageView.as_view(), name='help'),
                       url(r'^terms/$', TermsPageView.as_view(), name='terms'),
                       url(r'^privacy/$', PrivacyPageView.as_view(), name='privacy'),

)