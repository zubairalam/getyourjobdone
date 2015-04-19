from django.conf.urls import patterns, url

from .views import JobDetailView, JobListView


urlpatterns = patterns('',
                       url(r'^$', JobListView.as_view(), name='list'),
                       url(r'^(?P<slug>[^\.]+)/$', JobDetailView.as_view(), name='detail'),
)

