__author__ = 'lex'
from django.conf.urls.defaults import patterns, url
from testproj.testappp.views import BioView, RequestView, EditBioView
urlpatterns = patterns('',
    url(r'^$', BioView.as_view(),
        kwargs={'pk': 1}, name='bio-view'),
    url('^requests/$', RequestView.as_view(),
        kwargs={'page': 1}, name='requests-view'),
    url('^editbio/$', EditBioView.as_view(),
        kwargs={'pk': 1}, name='edit-bio'),
)
