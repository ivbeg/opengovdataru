import sys, os, re
import datetime
import chardet
import csv
import hashlib
from eventlet import httpc
from persimmon.contrib.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, Tag, NavigableString

from opendata.sources.common import *
from lxml import etree
try:
    from lxml.html import fromstring
except:
    pass
from StringIO import StringIO
from persimmon.contrib.html5lib import treebuilders, html5parser, sanitizer
from urlparse import urljoin        
import xml.etree.ElementTree as ET



datapath = '/var/www/export.opengovdata.ru/html/data/0.1/zakupki.gov.ru/Nomenklatura/'
rawpath = datapath + 'raw/'


def produceOpenDataXML(fields, data, filename, template):
    soup = BeautifulSoup(open(template, 'r').read(), fromEncoding='utf8')
#    print soup
    table = soup.find('table')
    for i in range(0, len(data)):
	row = Tag(soup, 'row')
	table.insert(i, row)
	for cn in range(0, len(fields)):
	    col = Tag(soup, 'col')	    
	    col['num'] = str(cn+1)
	    text = NavigableString(unicode(data[i][fields[cn]]).replace('\n', ' ').strip())
	    row.insert(cn, col)
	    col.insert(0, text)
    f = open(filename, 'w')	    
    f.write(soup.prettify())
    f.close()
    pass
    

def produceData(fields, data, filename, format="CSV", template=None):
    if format == 'openDataXML':
	return produceOpenDataXML(fields, data, filename, template)
    if format == 'CSV':
	sep = ';'
    elif format == 'TSV':
	sep = '\t'
    f = open(filename, 'w')
    s = sep.join(fields) + u'\n'
    f.write(s.encode('utf8'))
    for item in data:
	rec = []
	for field in fields:
	    rec.append(unicode(item[field]).replace('\n', ' ').strip())
	s = sep.join(rec) + u'\n'
	f.write(s.encode('utf8'))
    f.close()
	
    

class NomenklaturaExtractor(OpenDataExtractor):
	fields = ['code', 'measure', 'name', 'level', 'parent', 'type']
	sourceid = 'zakupki_gov_ru_Nomenklatura'
	urlpath = 'http://export.opengovdata.ru/data/0.1/zakupki.gov.ru/Nomenklatura/'
        
	filename = os.path.join(rawpath, 'snomen.csv')
    
	def __init__(self):
		pass
	
    
	def parse(self):
		return self.readFile(self.filename)

	def __guess_level(self, code):
		if len(code) == 8:
			level = 1
		elif len(code) == 12:
			level = 2
		if len(code) == 2:
			level  = 3
		elif len(code) == 4:
			level = 4
		elif len(code) == 9:
			(p1, p2, p3) =  code.split('.')
			if p3 == '000':
				level = 5 
			elif p3[2] == '0':
				level = 6
			else:
				level = 7
		return level

	def readFile(self, filename):
		print filename
		data = []
		i = 0
		reader = csv.reader(open(self.filename, 'r'), delimiter=';', quotechar='"')
		parents = {}
		for item in reader:		
			i += 1
			rec = {}
			rec['code'] = unicode(item[0].decode('windows-1251'))
			rec['measure'] = unicode(item[1].decode('windows-1251'))
			rec['name'] = unicode(item[2].decode('windows-1251'))
			level = self.__guess_level(rec['code'])
			rec['level'] = level
			rec['type'] = unicode(item[3].decode('windows-1251'))
			parents[level] = rec['code']
			if level == 1:
				parent = ''
			else:
				parent = parents.get(level-1, '')
			rec['parent'] = parent
			data.append(rec)
		return data
	    

	def updateSpec(self, files):
		template = os.path.join(datapath, 'opendata.tmpl')
		tree = ET.parse(template)
		current = tree.find('data/current')
		specid = tree.find('specs/tablespec').attrib['id']
		i = 0
		for f in files:
			elem = ET.SubElement(current, 'tableref')
			elem.set('type', f['type'])
			elem.set('format', f['format'])
			elem.set('specid', specid)
			elem.set('date_updated', f['date_updated'].isoformat())
			m = hashlib.sha512()
			m.update(open(f['filename'], 'r').read())
			elem.set('hash_sha512', m.hexdigest())
			elem.set('url', self.urlpath + os.path.basename(f['filename']))	    
			i += 1
		filename = os.path.join(datapath, 'opendata.xml')
		tree.write(filename, encoding='utf8')	
	
	def process(self):
		objects = self.readFile(self.filename)
		files = []

		produceData(self.fields, objects, os.path.join(datapath, self.sourceid+'.csv'), format="CSV", template=None)	
		files.append({'filename' : os.path.join(datapath, self.sourceid+'.csv'), 'type' : 'full', 'date_updated' : datetime.datetime.now(), 'format' : 'CSV'})
	
		produceData(self.fields, objects, os.path.join(datapath, self.sourceid+'.tsv'), format="TSV", template=None)
		files.append({'filename' : os.path.join(datapath, self.sourceid+'.tsv'), 'type' : 'full', 'date_updated' : datetime.datetime.now(), 'format' : 'TSV'})

		produceData(self.fields, objects, os.path.join(datapath, self.sourceid+'.xml'), format="openDataXML", template=os.path.join(datapath, 'opendatatable.tmpl'))
		files.append({'filename' : os.path.join(datapath, self.sourceid+'.xml'), 'type' : 'full', 'date_updated' : datetime.datetime.now(), 'format' : 'openDataXML'})
	
		self.updateSpec(files)
	
	
if __name__ == "__main__":
    ex = NomenklaturaExtractor()
    ex.process()
	
	
    