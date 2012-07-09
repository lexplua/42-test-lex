from django.views.generic import DetailView, ListView
from testproj.testappp.models import *


class BioView(DetailView):
    model = BioModel
    template_name = 'info.html'
    context_object_name = 'bio'


class RequestView(ListView):
    model = RequestModel
    context_object_name = 'requests'
    template_name = 'middleware_request.html'
    paginate_by = 10
