from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url('', include('apps.core.urls', namespace='core')),

                       url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^companies/', include('apps.organisations.urls', namespace='organisations')),
                       url(r'^registration/', include('apps.registration.urls')),
                       url(r'^search/', include('haystack.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
