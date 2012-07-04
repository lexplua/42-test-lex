from django.views.generic import DetailView
from testproj.testappp.models import *

class BioView(DetailView):
    model = BioModel
    template_name = 'info.html'
    context_object_name = 'bio'
