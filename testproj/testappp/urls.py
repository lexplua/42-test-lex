__author__ = 'lex'
from django.conf.urls.defaults import patterns, url
from testproj.testappp.views import BioView
urlpatterns = patterns('',
    url(r'',BioView.as_view(),kwargs={'pk':1},name='bio-view'),
)