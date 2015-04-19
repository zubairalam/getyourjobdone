from django.conf.urls import url, patterns
from .views import UserLocalRegistrationWizardView

registration_view = UserLocalRegistrationWizardView.as_view(UserLocalRegistrationWizardView.FORMS,
        url_name='local_registration_step', done_step_name='local_registration_finished')

urlpatterns = patterns('',
                url(r'^local_registration/(?P<step>.+)/$', registration_view, name='local_registration_step'),
                url(r'^local_registration/$',registration_view, name='local_registration'),
                )

