# -*- coding:utf8 -*-
"""
Russian government blogs aggregator
Ivan Begtin
apiviews.py
"""

import simplejson
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseRedirect
from StringIO import StringIO
import csv

from opendata import models

DATASOURCE_ATTRS = ['slug', 'name', 'about_txt', 'language', 'description_link', 'permanent_link', 'date_created']
OPENDATA_ATTRS = ['slug', 'name', 'description', 'language', 'opendata_id', 'opendata_url', 'location_url', 'spec_id', 'date_created']
BASE_URL = 'http://www.opengovdata.ru'



def __format_data(data, format='json', keys=None, params = {}):
    """Returns data using specific format CSV or JSON"""
    if format == 'csv':
        io = StringIO()
        wr = csv.writer(io, dialect='excel')
        for r in data:
            row = []
            for k in keys:
                row.append(r[k])
            wr.writerow(row)
            value = io.getvalue()
        return HttpResponse(value, mimetype="text/csv")
    elif format == 'json':
        s = simplejson.dumps(data, indent=4)
        value = u'\n'.join([l.rstrip() for l in  s.splitlines()])
        return HttpResponse(value, mimetype="application/json")
    else:   # by default - return JSON data
        s = simplejson.dumps(data, indent=4)
        value = u'\n'.join([l.rstrip() for l in  s.splitlines()])
        return HttpResponse(value, mimetype="application/json")
        
@cache_page(60 * 15)
def api_get_all_sources(request):
    """Returns all of data sourcs"""
    format = request.GET.get('format', 'json')
    d = []
    for o in models.DataSource.objects.order_by('-date_created'):
        item = {}
        for attr in DATASOURCE_ATTRS:
            a = getattr(o, attr)
            item[attr] = a.encode('utf8') if type(a) == type(u'') else a
        item['date_created'] = item['date_created'].isoformat()
        item['opengovdata_url'] = BASE_URL + o.get_absolute_url()
        item['organization_name'] = o.organization.name if o.organization else ""
        item['organization_website'] = o.organization.website if o.organization else ""
        item['datatypes'] = [dt.name for dt in o.datatype.all()]
        item['formats'] = [dt.name for dt in o.formats.all()]
        if format == 'csv':
            item['datatypes'] = u' '.join(item['datatypes'])
            item['formats'] = u' '.join(item['formats'])
        d.append(item)
    if format == 'csv':
        keys = []
        keys.extend(DATASOURCE_ATTRS)
    else:
        keys = None
    response = __format_data(d, format=format, keys=keys)
    return response

@cache_page(60 * 15)
def api_get_all_datasets(request):
    """Returns all of datasets"""
    format = request.GET.get('format', 'json')
    d = []
    for o in models.OpenData.objects.order_by('-date_created'):
        item = {}
        for attr in OPENDATA_ATTRS:
            a = getattr(o, attr)
            item[attr] = a.encode('utf8') if type(a) == type(u'') else a
        item['date_created'] = item['date_created'].isoformat()
        item['opengovdata_url'] = BASE_URL + o.get_absolute_url()
        item['organization_name'] = o.organization.name if o.organization else ""
        item['organization_website'] = o.organization.website if o.organization else ""
        item['datatypes'] = [dt.name for dt in o.datatypes.all()]
        item['formats'] = [dt.name for dt in o.formats.all()]
        if format == 'csv':
            item['datatypes'] = u'|'.join(item['datatypes'])
            item['formats'] = u'|'.join(item['formats'])
        d.append(item)
    if format == 'csv':
        keys = []
        keys.extend(OPENDATA_ATTRS)
    else:
        keys = None
    response = __format_data(d, format=format, keys=keys)
    return response
