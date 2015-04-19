from django.views.generic import DetailView, ListView
from core.models import PublishableModel
from apps.jobs.models import Job


class JobDetailView(DetailView):
    template_name = 'jobs/detail.jade'
    model = Job
    slug_url_kwarg = 'slug'


class JobListView(ListView):
    template_name = 'jobs/list.jade'
    queryset = Job.objects.filter(published_status=PublishableModel.PUBLISHED_STATUS.Published).order_by('-created')


