# -*- coding:utf8 -*-
"""
OpenData
Ivan Begtin
views.py
"""

from django.utils import feedgenerator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.cache import patch_vary_headers
from django.template import Context, loader, RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.utils.xmlutils import SimplerXMLGenerator
from django.conf import settings
from django.core.cache import cache

from djlinks import models
import sys

import traceback, datetime
import urlparse
import md5
import simplejson

def newslist_view(request):
    """Просмотр списка новостей"""
    queryset = models.NewsEntry.objects.all().order_by('-pubdate')
    params = {'base_url' : '/news/', 'total' : len(queryset)}
    return object_list(request, queryset, template_name='djlinks/news.html', paginate_by=10, allow_empty=True, extra_context=params)
#    return render_to_response('catalog.html', params)



def news_view(request, obj_id):
    """Просмотр новости"""
    queryset = models.NewsEntry.objects.all()
    params = {'base_url' : '/news/', 'total' : len(queryset)}
    return object_detail(request, queryset, object_id=obj_id, template_name='djlinks/news_item.html', extra_context=params)
                
def newsrss_view(request):
    """Просмотр RSS новости"""
    from django.utils import feedgenerator
    f = feedgenerator.Atom1Feed(title=u'OpenGovData.ru. Новости', language=u"ru", link=u"http://opengovdata.ru/news/", description=u'OpenGovData.ru. Новости')
    objects = models.NewsEntry.objects.all().order_by('-pubdate')[0:20]
    for p in objects:
            f.add_item(title=p.title, link="http://opengovdata.ru/news/%s/" %(str(p.id)), description=p.body, pubdate=p.pubdate)
    return HttpResponse(f.writeString('utf8'), mimetype='text/xml;')
                                
                                                