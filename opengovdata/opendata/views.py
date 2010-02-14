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

from opendata import models
import sys

import traceback, datetime
import urlparse
import md5
import simplejson

def sourceslist_view(request):
    """Просмотр списка источников данных"""
    org_id = request.GET.get('org', '-1')
    q = request.GET.get('q', None)
    type_id = request.GET.get('type', '-1')
    format_id = request.GET.get('format', '-1')
    pkeys = []
    if q is None or (len(q) == 0) or q == u'None':
	q = None
    else:
	pkeys.append('q=%s' %(q))
    params = {'current_org' : None}
    org = None    
    try:
	org = models.Organization.objects.get(id=int(org_id))
	queryset = models.DataSource.objects.filter(organization=org)
	params['current_org'] = org.id
	pkeys.append('org=%s' %(org_id))
    except:	
	queryset = models.DataSource.objects.all()

    try:
	dtype = models.DataType.objects.get(id=int(type_id))
	queryset = queryset.filter(datatype=dtype)
	params['current_type'] = dtype.id
	pkeys.append('type=%s' %(type_id))
    except:	
	pass
    params['datatypes'] = models.DataType.objects.all().order_by('name')

    try:
	format = models.DataFormat.objects.get(id=int(format_id))
	queryset = queryset.filter(formats=format)
	params['current_format'] = format.id
	pkeys.append('format=%s' %(format_id))
    except:	
	pass
    params['formats'] = models.DataFormat.objects.all().order_by('name')
	
    if q:
	queryset = queryset.filter(name__contains=q).order_by('-id')          
	params['q'] = q
#	params['querystr'] = 'q=%s&org=%s' %(q, org_id)
    else:
	queryset = queryset.order_by('-id')          
    params['querystr'] = '&'.join(pkeys)
#	if org is not None:
#	    params['querystr'] = 'org=%s' %(org_id)
    orgs = models.Organization.objects.all().order_by('name')
    params.update({'base_url' : '/sources/', 'orgs': orgs, 'total' : len(queryset)})
    return object_list(request, queryset, template_name='opendata/sources.html', paginate_by=10, allow_empty=True, extra_context=params)

def sourcesrss_view(request):
    """Просмотр RSS списка источников данных"""
    from django.utils import feedgenerator
    f = feedgenerator.Atom1Feed(title=u'OpenGovData.ru. Источники данных', language=u"ru", link=u"http://opengovdata.ru/sources/", description=u'OpenGovData.ru. Источники данных')                                        
    objects = models.DataSource.objects.all().order_by('-date_created')[0:20]
    for p in objects:
	f.add_item(title=p.name, link="http://opengovdata.ru/source/%s/" %(str(p.id)), description=p.about_txt, pubdate=p.date_created)
    return HttpResponse(f.writeString('utf8'), mimetype='text/xml;')
                                                                    


def source_view(request, obj_id):
    """Просмотр источника данных"""
    queryset = models.DataSource.objects.all()
    params = {'base_url' : '/sources/', 'total' : len(queryset)}
    return object_detail(request, queryset, object_id=obj_id, template_name='opendata/source.html', extra_context=params)


import djlinks
def home_view(request):
    params = {}
    params['news'] = djlinks.models.NewsEntry.objects.all().order_by('-pubdate')[0:5]
    params['sources'] = models.DataSource.objects.all().order_by('-id')[0:5]
    return render_to_response('opendata/home.html', params)
#    return render_to_response('catalog.html', params)


def opendatarss_view(request):
    """Просмотр RSS списка открытых данных"""
    from django.utils import feedgenerator
    f = feedgenerator.Atom1Feed(title=u'OpenGovData.ru. Реестр открытых данных', language=u"ru", link=u"http://opengovdata.ru/opendata/", description=u'OpenGovData.ru. Открытые данных')                                        
    objects = models.OpenData.objects.all().order_by('-date_updated')[0:20]
    for p in objects:
	f.add_item(title=p.name, link="http://opengovdata.ru/opendata/%s/" %(str(p.id)), description=p.description, pubdate=p.date_created)
    return HttpResponse(f.writeString('utf8'), mimetype='text/xml;')


def opendatalist_view(request):
    """Просмотр списка открытых данных"""
    org_id = request.GET.get('org', '-1')
    q = request.GET.get('q', None)
    format_id = request.GET.get('format', '-1')
    pkeys = []
    if q is None or (len(q) == 0) or q == u'None':
	q = None
    else:
	pkeys.append('q=%s' %(q))
    params = {'current_org' : None}
    org = None    
    try:
	org = models.Organization.objects.get(id=int(org_id))
	queryset = models.OpenData.objects.filter(organization=org)
	params['current_org'] = org.id
	pkeys.append('org=%s' %(org_id))
    except:	
	queryset = models.OpenData.objects.all()


    try:
	format = models.DataFormat.objects.get(id=int(format_id))
	queryset = queryset.filter(formats=format)
	params['current_format'] = format.id
	pkeys.append('format=%s' %(format_id))
    except:	
	pass
    params['formats'] = models.DataFormat.objects.all().order_by('name')
	
    if q:
	queryset = queryset.filter(name__contains=q).order_by('-id')          
	params['q'] = q
#	params['querystr'] = 'q=%s&org=%s' %(q, org_id)
    else:
	queryset = queryset.order_by('-id')          
    params['querystr'] = '&'.join(pkeys)
    orgs = models.Organization.objects.all().order_by('name')
    params.update({'base_url' : '/sources/', 'orgs': orgs, 'total' : len(queryset)})
    return object_list(request, queryset, template_name='opendata/opendata_list.html', paginate_by=10, allow_empty=True, extra_context=params)


def opendata_view(request, obj_id):
    """Просмотр открытых данных"""
    queryset = models.OpenData.objects.all()
    params = {'base_url' : '/opendata/', 'total' : len(queryset)}
    return object_detail(request, queryset, object_id=obj_id, template_name='opendata/opendata.html', extra_context=params)
