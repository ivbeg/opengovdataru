#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import sys
import random
import md5
import os
import os.path
import time
import optparse
import datetime
import socket
import traceback
import re
import time

import signal, xml, urllib
from xml.dom.ext.reader import HtmlLib, Sgmlop, PyExpat
import xml.xpath
import re

from urllib2 import urlopen
from persimmon.contrib.BeautifulSoup import BeautifulSoup
from gnosis.xml.objectify import make_instance


class OpenDataImporter:
    def __init__(self):
	pass

    def import_map(self, urlpath):
	print 'Imporing OpenData index %s' %(urlpath)
	u = urlopen(urlpath)
	data = u.read()
	u.close()    
	odata = make_instance(data)
	
	for o in odata.opendata:
	    print 'Importing OpenDATA: %s' %(o.loc.PCDATA)
	    self.import_data(o.loc.PCDATA)
	
    def import_data(self, urlpath):
	from opendata import models
	u = urlopen(urlpath)
	data = u.read()
	u.close()    

	odata = make_instance(data)
#	odata.source.id
	slug = odata.source.id.replace('_', '-')   # To conform requrements for urls
	(opendata, created) = models.OpenData.objects.get_or_create(slug=slug)
	opendata.slug = slug
	opendata.opendata_id = odata.source.id
	if hasattr(odata.source, 'location'):
	    opendata.location_url = odata.source.location.PCDATA
	opendata.opendata_url = urlpath
	opendata.name = odata.source.name.PCDATA
	opendata.description = odata.source.description.PCDATA
	opendata.language = odata.source.language.PCDATA
	opendata.dinfo_isupdatable = (odata.datainfo.datatype.is_updatable != 'False')
	opendata.date_created = datetime.datetime.strptime(odata.datainfo.created.PCDATA, "%Y-%m-%dT%H:%M:%SZ")
	opendata.date_updated = datetime.datetime.strptime(odata.datainfo.updated.PCDATA, "%Y-%m-%dT%H:%M:%SZ")
	opendata.author_name = odata.datainfo.preparedBy.author.PCDATA
	opendata.author_website = odata.datainfo.preparedBy.authorWebsite.PCDATA
	
	# Import organization
	orgname = odata.source.org.name.PCDATA
	(org, created) = models.Organization.objects.get_or_create(name=orgname)
	if created:
	    org.description = odata.source.org.description.PCDATA
	    org.website = odata.source.org.website.PCDATA
	    org.address = odata.source.org.address.PCDATA
	    org.save()	

	opendata.organization = org
	opendata.spec_id = odata.specs.tablespec.id
	opendata.save()
	    
	opendata.fields().delete()
	for ofield in odata.specs.tablespec.cols.colspec:
	    try:
		field = models.DataField.objects.get(opendata=opendata, key=ofield.key)
	    except:
		field = models.DataField(num=ofield.num, name=ofield.name.PCDATA, opendata=opendata)
	    field.description = ofield.description.PCDATA
	    field.key = ofield.key
	    field_type = ofield.type
	    ftype = models.FieldType.objects.get(name=field_type)
	    field.field_type = ftype
	    field.save()
	    pass

	opendata.files().delete()
	for tableref in odata.data.current.tableref:	
	    try:
		dfile = models.OpenDataFile.objects.get(opendata=opendata, urlpath=tableref.url)
	    except:
		format = models.DataFormat.objects.get(name=tableref.format)
		datatype = models.OpenDataType.objects.get(key=tableref.type)
		opendata.datatypes.add(datatype)
		opendata.formats.add(format)
		dfile = models.OpenDataFile(opendata=opendata, urlpath=tableref.url, format=format, datatype=datatype, hash_sha512=tableref.hash_sha512)
		dfile.specid = tableref.specid
		parts = tableref.date_updated.rstrip('Z').rsplit('.', 1)
		gt = parts[0]
		try:
		    dfile.date_updated = datetime.datetime.strptime(gt, "%Y-%m-%dT%H:%M:%S")
		except:
		    dfile.date_updated = datetime.datetime.strptime(gt, "%Y-%m-%dT%H:%M:%SZ")
		    
	    dfile.save()
	    
	
	

def import_opendata_xml(urlpath):
    odi = OpenDataImporter()
    odi.import_map(urlpath)
    

def main():
    """ Main function. Nothing to see here. Move along.
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

    import_opendata_xml(sys.argv[1])	
    
if __name__ == '__main__':
    main()



