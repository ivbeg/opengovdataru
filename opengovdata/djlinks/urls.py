# -*- coding: utf-8 -*-

"""
classifier
Ivan Begtin
urls.py
"""

from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

from djlinks import views

urlpatterns = patterns('',
    (r'^news/$', views.newslist_view),            
    (r'^news/rss/$', views.newsrss_view),            
    (r'^news/(?P<obj_id>\d+)/$', views.news_view),
        
)
