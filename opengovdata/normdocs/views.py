# -*- coding:utf8 -*-
"""
OpenData: NormDocs
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

from normdocs import models
import sys

import traceback, datetime
import urlparse
import md5
import simplejson

def docslist_view(request):
    """Просмотр списка источников данных"""
    org_id = request.GET.get('org', '-1')
    q = request.GET.get('q', None)
    type_id = request.GET.get('type', '-1')
    format_id = request.GET.get('format', None)
    theme_id = request.GET.get('theme', '-1')
    
    pkeys = []
    if q is None or (len(q) == 0) or q == u'None':
	q = None
    else:
	pkeys.append('q=%s' %(q))
    params = {'current_org' : None}
    org = None    
    try:
	org = models.Organization.objects.get(id=int(org_id))
	if org is not None:
	    queryset = models.Document.objects.filter(organization=org)
	    params['current_org'] = org.id
	    pkeys.append('org=%s' %(org_id))
	else:
	    queryset = models.Document.objects.all().order_by('-date_created')
    except:	
	queryset = models.Document.objects.all().order_by('-date_created')

    try:
	dtype = models.DocumentType.objects.get(id=int(type_id))
	queryset = queryset.filter(doctype=dtype)
	params['current_type'] = dtype.id
	pkeys.append('type=%s' %(type_id))
    except:	    
	pass

    params['datatypes'] = models.DocumentType.objects.all().order_by('name')
    params['themes'] = models.DocumentTheme.objects.all().order_by('name')
    if format_id is not None:
	queryset = queryset.filter(format=format_id)
	params['current_format'] = format_id
	pkeys.append('format=%s' %(format_id))
    params['formats'] = models.DOCUMENT_FORMATS

    try:
	theme = models.DocumentTheme.objects.get(id=int(theme_id))
	queryset = queryset.filter(theme=theme)
	params['current_theme'] = theme.id
	pkeys.append('theme=%s' %(theme_id))
    except:	
	pass
	
    if q is not None:
	queryset = queryset.filter(name__contains=q).order_by('-id')          
	params['q'] = q
    else:
	queryset = queryset.order_by('-id')          
    params['querystr'] = '&'.join(pkeys)
#    queryset =  models.Document.objects.all()
    orgs = models.Organization.objects.all().order_by('name')
    params.update({'base_url' : '/laws/', 'orgs': orgs, 'total' : len(queryset)})
    return object_list(request, queryset, template_name='normdocs/doc_list.html', paginate_by=10, allow_empty=True, extra_context=params)

def docsrss_view(request):
    """Просмотр RSS списка источников данных"""
    from django.utils import feedgenerator
    f = feedgenerator.Atom1Feed(title=u'OpenGovData.ru. Документы', language=u"ru", link=u"http://opengovdata.ru/laws/", description=u'OpenGovData.ru. Документы')                                        
    objects = models.Document.objects.all().order_by('-date_created')[0:20]
    for p in objects:
	f.add_item(title=p.name, link="http://opengovdata.ru/laws/%s/" %(str(p.id)), description=p.description, pubdate=p.date_created)
    return HttpResponse(f.writeString('utf8'), mimetype='text/xml;')
                                                                    


def document_view(request, obj_id):
    """Просмотр источника данных"""
    queryset = models.Document.objects.all()
    params = {'base_url' : '/laws/', 'total' : len(queryset)}
    return object_detail(request, queryset, object_id=obj_id, template_name='normdocs/doc.html', extra_context=params)


