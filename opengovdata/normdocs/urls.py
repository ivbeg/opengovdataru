# -*- coding: utf-8 -*-

"""
OpenData
Ivan Begtin
urls.py
"""

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to, direct_to_template
from django.utils.translation import gettext_lazy as _

from normdocs import views, models



urlpatterns = patterns('',
    (r'^laws/$', views.docslist_view),
    (r'^laws/rss/$', views.docsrss_view),
    (r'^laws/(?P<obj_id>\d+)/$', views.document_view),
    )
