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
from urlgrabber import urlopen
import re

import pycurl

import httplib, email.utils, time,datetime, urlparse



def striplist(l, ch=None):
    if ch is not None:
	return([x.strip(ch) for x in l])
    else:
	return([x.strip(ch) for x in l])

def import_tags():    
    print 'Imporing tags'
    from opendata import models
#    models.Tag.objects.all().delete()
    f = open('datasources.tsv', 'r')
    lines = f.read().splitlines()
    f.close()
    alltags = []
    for line in lines:
	line = line.strip().decode('utf8')
	if len(line) == 0:
	    continue
	parts = line.split(u'\t')
	if len(parts) > 3:
	    tags = striplist(striplist(parts[3].split(',')), u'"')
	    for tag in tags:
		if tag not in alltags:
		    alltags.append(tag)
		    
    for tag in alltags:    
	objs = models.Tag.objects.filter(name=tag)
	if len(objs) == 0:
	    o = models.Tag(name=tag)
	    o.save()
	print tag	

def import_formats():
    print 'Imporing formats'
    from opendata import models
    f = open('datasources.tsv', 'r')
    lines = f.read().splitlines()
    f.close()
    for line in lines:
	line = line.strip().decode('utf8')
	if len(line) == 0:
	    continue
	parts = line.split(u'\t')
	if len(parts) > 6:
	    formats = striplist(striplist(parts[6].split(',')), u'"')
	    for format in formats:
	        objs = models.DataFormat.objects.filter(name=format)
		if len(objs) == 0:
		    o = models.DataFormat(name=format)
		    o.save()

def import_types():
    from opendata import models
    print 'Imporing types'
    f = open('datasources.tsv', 'r')
    lines = f.read().splitlines()
    f.close()
    for line in lines:
	line = line.strip().decode('utf8')
	if len(line) == 0:
	    continue
	parts = line.split(u'\t')
	if len(parts) > 5:
#	    print parts[5]
	    objs = models.DataType.objects.filter(name=parts[5])
	    if len(objs) == 0:
		o = models.DataType(name=parts[5])
		o.save()
    
def import_sources():
    print 'Imporing sources'
    from opendata import models
    models.DataSourceTag.objects.all().delete()
    models.DataSource.objects.all().delete()
    f = open('datasources.tsv', 'r')
    lines = f.read().splitlines()
    f.close()
    for line in lines:
	line = line.strip().decode('utf8')
	if len(line) == 0:
	    continue
	parts = line.split(u'\t')	
	if len(parts) > 3:
	    tags = striplist(striplist(parts[3].split(',')), u'"')
	    if u'russia' in tags and u'government' in tags:
		pass
	    else:
		continue
	    name = parts[0].strip().strip('"').strip()
	    objs = models.DataSource.objects.filter(name=name)
	    if len(objs) == 0:		
		description = parts[2].strip().strip('"').strip()
		url = parts[1].strip().strip('"').strip()
		if url[0:7] == u'http://':
		    if len(url) > 57:
			slug = url[len(url)-55:len(url)-1].replace(u'.', u'_').replace(u'/', u'-')
		    else:
			slug = url[7:56].replace(u'.', u'_').replace(u'/', u'-')
		    print slug
		try:
		    o = models.DataSource(slug=slug, name=name, description_link=url, permanent_link=url, about_txt=description)
		    o.save()
		except:
		    o = models.DataSource(slug=slug+'_' + str(random.random()), name=name, description_link=url, permanent_link=url, about_txt=description)
		    o.save()
	    else:
		o = objs[0]	    
	    for tag in tags:
		tobj = models.Tag.objects.get(name=tag)
		try:
		    tlink = models.DataSourceTag.objects.get(source=o, tag=tobj)
		except:
		    tlink = models.DataSourceTag(source=o, tag=tobj)
		    tlink.save()		

	    if len(parts) > 5:
		tobj = models.DataType.objects.get(name=parts[5].strip())
		if tobj not in o.datatype.all():
		    o.datatype.add(tobj)
	    if len(parts) > 6:
		formats = striplist(striplist(parts[6].split(',')), u'"')
	        for format in formats:
	    	    fobj = models.DataFormat.objects.get(name=format)
	    	    if fobj not in o.formats.all():
	    		o.formats.add(fobj)
	    

def update_slugs():
    from opendata import models
    for source in models.DataSource.objects.all():
	source.slug = str(source.id)
	source.save()

def main():
    """ Main function. Nothing to see here. Move along.
    """
    parser = optparse.OptionParser(usage='%prog [options]', version="0.0.1")
    parser.add_option('--settings', \
      help='Python path to settings module. If this isn\'t provided, the DJANGO_SETTINGS_MODULE enviroment variable will be used.')

    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', \
      default=False, help='Verbose output.')
    options = parser.parse_args()[0]
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    else:
	os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

    from opendata import models
    for item in models.DataSource.objects.all():
	l = []
	print len(item.tags())
	for tag in item.tags():
#	    print tag
	    l.append(tag.tag.name)
	s = ', '.join(l)
#	print s
	
#    import_tags()
#    import_types()
#    import_formats()
#    import_sources()
#    update_slugs()
#    list_feeds()        

#    do_test('urls_orgs.txt')        
#    export_spam()
    
if __name__ == '__main__':
    main()



