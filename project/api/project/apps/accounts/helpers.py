from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login

def logout_required(view):
    """
    Decorator makes sure user has to be logged out.
    """
    def f(request, *args, **kwargs):
        if request.user.is_anonymous():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return f


def login(request, *args, **kwargs):
    """
    Making sure to remember the user
    """
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_login(request, *args, **kwargs)


def secure_required(view_func):
    """
    Decorator makes sure URL is accessed over https.
    """
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func