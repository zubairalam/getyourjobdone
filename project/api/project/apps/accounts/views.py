import re
import uuid
import requests
import json

from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.core.validators import ValidationError, validate_email
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.dispatch import receiver
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponseRedirect, render, render_to_response
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View, TemplateView
from allauth.account.signals import *

from apps.accounts.models import UserProfile
from apps.core.helpers import send_mail, image_downloader
from apps.profile.social_profile import Profile
from .forms import LoginForm, RegistrationForm, ResetPasswordForm
from .helpers import logout_required, login


@receiver(user_logged_in)
def social_user_profile(sender, **kwargs):
    user = kwargs['user']
    try:
        user_profile = UserProfile.objects.get(user=user)
        # update local_user_profile, linkedin_profile or facebook_profile
        Profile.update_profile(user)
    except ObjectDoesNotExist:
        from allauth.socialaccount.models import SocialAccount, SocialToken

        try:
            social_account = SocialAccount.objects.get(user=user)
            social_token = SocialToken.objects.get(account=social_account)
            token = social_token.token
            provider = social_account.get_provider().id
            Profile.create_social_profile(provider=provider, user=user, token=token)
        except Exception as e:
            print(e)


class LoginView(FormView):
    """
    The Local Login View.
    """
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form, **kwargs):
        if form.is_valid():
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:dashboard')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['state'] = uuid.uuid1()
        return context

    @method_decorator(logout_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


class LogoutView(TemplateView):
    """
    The Logout View.
    """
    template_name = 'accounts/logout.html'

    def render_to_response(self, context, **response_kwargs):
        try:
            logout(self.request)
        except:
            raise Http404
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   **response_kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)


class RegistrationView(FormView):
    """
    The Local Registration View.
    """
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:registration_success')

    def form_valid(self, form, **kwargs):
        user = form.save()
        self.send_registration_mail(user)
        return HttpResponseRedirect(self.get_success_url())

    def send_registration_mail(self, user):
        recipients = [user.email]
        email_template = 'registration_confirmation'
        link = "{0}{1}{2}{3}".format("https://" if self.request.is_secure() else "http://",
                                     "".join(get_current_site(self.request).domain),
                                     reverse('accounts:registration_confirmation'), str(user.hash))
        user_profile = UserProfile.objects.get(user=user)
        context = {
            'name': " ".join([user_profile.first_name, user_profile.last_name]),
            'site': get_current_site(self.request).name,
            'registration_link': link
        }
        send_mail(recipients, email_template, context)

    @method_decorator(logout_required)
    def dispatch(self, *args, **kwargs):
        return super(RegistrationView, self).dispatch(*args, **kwargs)


class RegistrationSuccess(TemplateView):
    """
    If Registration is successful.
    """
    template_name = 'accounts/registration_success.html'


class RegistrationFailure(TemplateView):
    """
    If Registration is not successful.
    """
    template_name = 'accounts/registration_failure.html'


class RegistrationConfirmation(View):
    """
    Retrieve hash key from mailed registration link clicked by the user,
    check if a user exists with that hash key
    If True then make user account active
    """

    def get(self, request):
        try:
            m = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', request.path)
            h = m.group(0)
            user = get_user_model().objects.get(hash=str(h))
            # once a hash is matched, corresponding user.hash should be rehashed, so previous hash never be misused
            user.hash = uuid.uuid1()
            user.active = True
            user.save()
            return HttpResponseRedirect(reverse('accounts:registration_success'))
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            return HttpResponseRedirect(reverse('accounts:registration_failure'))
        except Exception:
            return HttpResponseRedirect(reverse('accounts:registration_failure'))


class ResendConfirmationLink(View):
    """
    Resend confirmation if email is not confirmed with JobPlus i.e. user.active = True
    """

    def post(self, request):
        if request.is_ajax():
            email = request.POST.get("email", "")
            try:
                validate_email(email)
            except ValidationError:
                return HttpResponse("Enter a valid email address")
            try:
                user = get_user_model().objects.get(email=email)
                user.hash = uuid.uuid1()
                user.save()
                recipients = [user.email]
                email_template = 'registration_confirmation'
                link = "{0}{1}{2}{3}".format("https://" if self.request.is_secure() else "http://",
                                             "".join(get_current_site(self.request).domain),
                                             reverse_lazy('accounts:registration_confirmation'), str(user.hash))
                context = {
                    'name': user.get_full_name(),
                    'site': get_current_site(self.request).name,
                    'registration_link': link
                }
                send_mail(recipients, email_template, context)
                return HttpResponse("success")
            except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
                return HttpResponse("failure")
        else:
            raise Http404

    def get(self, request):
        return render(request, self.get_template_name())

    def get_template_name(self):
        return 'accounts/resend_email_confirmation.html'


class SendPasswordResetLink(View):
    def get(self, request):
        return render(request, self.get_template_name())

    def get_template_name(self):
        return 'accounts/verify_email.html'

    def post(self, request):
        email = request.POST.get("email", "")
        try:
            validate_email(email)
            try:
                user = get_user_model().objects.get(email__exact=email)
                if user.active:
                    # send a mail to him containing a reset password link
                    user.hash = uuid.uuid1()
                    user.save()
                    recipients = [user.email]
                    email_template = 'reset_password'
                    link = "{0}{1}{2}{3}".format("https://" if self.request.is_secure() else "http://",
                                                 "".join(get_current_site(self.request).domain),
                                                 reverse_lazy('accounts:reset_password'), str(user.hash))
                    context = {
                        'name': user.get_full_name(),
                        'site': get_current_site(self.request).name,
                        'reset_password_link': link
                    }
                    send_mail(recipients, email_template, context)
                    return HttpResponse("success")
                else:
                    # user is not active :: resend a confirmation mail, give him a link
                    return HttpResponse("failure")
            except ObjectDoesNotExist:
                # if email doesn't exist :: <a href="accounts:registration"> register here </a>
                return HttpResponse("email not found")
        except ValidationError:
            return HttpResponse("invalid email")
        except Exception as e:
            return HttpResponse("error")


class ResetPassword(FormView):
    template_name = 'accounts/reset_password.html'
    error_template = 'accounts/resetpw_failure.html'
    success_url = reverse_lazy('accounts:resetpw_success')
    form_class = ResetPasswordForm
    hash = ""

    def get(self, request, *args, **kwargs):
        # catch exception
        try:
            m = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', self.request.path)
            self.hash = m.group(0)
            user = get_user_model().objects.get(hash=str(self.hash))
        except:
            return render(request, self.error_template)
        return super(ResetPassword, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        hash = self.request.POST.get('hash', "")
        # try:
        if hash != "":
            user = get_user_model().objects.get(hash=hash)
            user = form.save(commit=False, user=user)
            user.hash = uuid.uuid1()
            user.save()
        #except Exception:
        #    return render(self.request, self.error_template)
        return super(ResetPassword, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ResetPassword, self).get_context_data(**kwargs)
        context['hash'] = self.hash
        return context


class ResetPasswordSuccess(TemplateView):
    template_name = 'accounts/resetpw_success.html'


class ForgotPassword(TemplateView):
    template_name = 'accounts/forgot_password.html'


class DashboardView(TemplateView):
    """
    The Default Dashboard View.
    """
    # template_name = 'accounts/dashboard.html'
    template_name = 'accounts/dashboard.html'

    def render_to_response(self, context, **response_kwargs):
        # session_user = self.request.user.id
        # context["me"] = User.objects.get(pk=session_user)
        user_profile = self.request.user.get_profile()
        if user_profile.gender == 1:
            user_profile.gender = 'Male'
        elif user_profile.gender == 2:
            user_profile.gender = 'Female'
        else:
            user_profile.gender = 'Other'
        user_profile.socials = self.request.user.get_social_accounts()
        context['user_profile'] = user_profile
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   **response_kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)
