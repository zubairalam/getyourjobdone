from django.views.generic import DetailView, ListView

from apps.core.models import PublishableModel

from .models import Organisation


class OrganisationDetailView(DetailView):
    template_name = 'organisations/detail.html'
    model = Organisation
    slug_url_kwarg = 'slug'


class OrganisationListView(ListView):
    template_name = 'organisations/list.html'
    queryset = Organisation.objects.filter(published=PublishableModel.PUBLISHED_STATUS.Live).order_by('-created')



