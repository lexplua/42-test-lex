from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from  django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('testproj.testappp.urls')),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'),
)
urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        }),
)
