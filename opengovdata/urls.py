from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('opendata.urls')),
    (r'', include('djlinks.urls')),
    (r'', include('normdocs.urls')),
#    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
#    (r'^account/', include('django_authopenid.urls')),
    (r'^admin/(.*)', admin.site.root),
)
            