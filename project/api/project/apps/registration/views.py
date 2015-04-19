import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView

from django.shortcuts import render
from .forms import *

class UserLocalRegistrationWizardView(NamedUrlSessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images/users'))

    FORMS = [('signup', RegistrationForm),
            ('upload_photo', UploadProfilePhotoForm)]

    TEMPLATES = {'signup':'signup.html',
                'upload_photo':'upload_photo.html'}

    @staticmethod
    def validate_photo(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('upload_photo') or {'method':'none'}
        print cleaned_data

    form_list = [RegistrationForm, UploadProfilePhotoForm]

    condition_dict = {'upload_photo': validate_photo}

    def get_template_names(self):
        return [UserLocalRegistrationWizardView.TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # create user profile using form_list validated data
        # first create a user account
        # then create a user profile
        self.create_user_and_user_profile(form_list, **kwargs)
        return render(self.request, 'done.html')

    def create_user_and_user_profile(self, form_list, **kwargs):
        signup_form = form_list[0]
        signup_form.save()


