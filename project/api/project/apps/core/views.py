from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = 'core/about.html'


class ContactPageView(TemplateView):
    template_name = 'core/contact.html'


class HelpPageView(TemplateView):
    template_name = 'core/help.html'


class HomePageView(TemplateView):
    template_name = 'core/home.html'


class PrivacyPageView(TemplateView):
    template_name = 'core/privacy.html'


class TermsPageView(TemplateView):
    template_name = 'core/terms.html'



