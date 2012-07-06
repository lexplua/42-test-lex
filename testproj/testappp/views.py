from django.utils.decorators import method_decorator
from django.views.generic import DetailView,ListView,UpdateView
from django.contrib.auth.decorators import login_required
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

class EditBioView(UpdateView):
    model = BioModel
    template_name = 'edit_bio.html'
    success_url = '/'
    context_object_name = 'bio'
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditBioView,self).dispatch(request, *args, **kwargs)
