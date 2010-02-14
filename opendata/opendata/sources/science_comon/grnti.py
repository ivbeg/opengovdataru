import sys, os, re
import datetime
import chardet
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



datapath = '/var/www/export.opengovdata.ru/html/data/0.1/science_common/GRNTI/'
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
	
    

class GrntiExtractor(OpenDataExtractor):
	fields = ['code', 'name', 'level']
	sourceid = 'science_common_grnti'
	urlpath = 'http://export.opengovdata.ru/data/0.1/science_common/GRNTI/'
        
	filename = os.path.join(rawpath, 'grnti.dbf')
    
	def __init__(self):
		pass
	
    
	def parse(self):
		return self.readFile(self.filename)

	def readFile(self, filename):
		print filename
		data = []
		from dbfpy import dbf
		
		reader = dbf.Dbf(filename, new=False)
		i = 0
		for item in reader:		
			i += 1
			rec = {}
			rec['code'] = unicode(item[0])
			rec['name'] = unicode(item[1].decode('windows-1251'))
			level = int(item[2].strip('_') )
			rec['level'] = level
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
    ex = GrntiExtractor()
    ex.process()
	
	
    