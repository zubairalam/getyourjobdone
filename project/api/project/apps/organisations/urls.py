from django.conf.urls import patterns, url

from .views import OrganisationDetailView, OrganisationListView


urlpatterns = patterns('',
                       url(r'^$', OrganisationListView.as_view(), name='list'),
                       url(r'^(?P<slug>[^\.]+)/$', OrganisationDetailView.as_view(), name='detail'),
)
