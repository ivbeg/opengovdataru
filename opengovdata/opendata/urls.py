# -*- coding: utf-8 -*-

"""
OpenData
Ivan Begtin
urls.py
"""

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to, direct_to_template
from django.utils.translation import gettext_lazy as _

from opendata import views, models



urlpatterns = patterns('',
    (r'^sources/$', views.sourceslist_view),
    (r'^sources/rss/$', views.sourcesrss_view),
    (r'^source/(?P<obj_id>\d+)/$', views.source_view),

    (r'^opendata/$', views.opendatalist_view),
    (r'^opendata/rss/$', views.opendatarss_view),
    (r'^opendata/(?P<obj_id>\d+)/$', views.opendata_view),
    
    url(r'^$', views.home_view),        
    url(r'^about/$', direct_to_template, {'template' : 'opendata/about.html'}),        
    url(r'^contacts/$', direct_to_template, {'template' : 'opendata/contacts.html'}),        
#    url(r'^laws/$', direct_to_template, {'template' : 'opendata/laws.html'}),        
#    url(r'^opendata/$', direct_to_template, {'template' : 'opendata/opendata.html'}),        
    )
