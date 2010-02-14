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



datapath = '/var/www/export.opengovdata.ru/html/data/0.1/roskazna.ru/TerrDepartments/'
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
	
    

class RoskaznaTerorgansExtractor(OpenDataExtractor):
    fields = ['num', 'name', 'address', 'chief', 'phone', 'fax']
    url = 'http://www.roskazna.ru/p/fk/ter_organs.html'    
    sourceid = 'roskazna_ru_TerrDepartments'
    urlpath = 'http://export.opengovdata.ru/data/0.1/roskazna.ru/TerrDepartments/'
        
    filename = os.path.join(rawpath, 'ter.xls')
    
    def __init__(self):
	pass
	
    def get(self, url):
        (status, headers, body) = httpc.get_(url, ok=[500, 501,300, 301, 503, 200, 404, 405])        
	return body
	
    
    def parse(self, data):
	# Locate url
	treebuilder = treebuilders.getTreeBuilder("etree", etree)
        p = html5parser.HTMLParser(tree=treebuilder)#, tokenizer=sanitizer.HTMLSanitizer)
        res = chardet.detect(data)
        if res and res.has_key('encoding'):
            encoding = res['encoding']
            
        if encoding is None:
            document = p.parse(StringIO(data))
        else:
	    document = p.parse(StringIO(data), encoding=encoding)
	d = document.xpath('//a[text()="XLS"]')
	if len(d) > 0:	    
	    url = d[0].attrib['href']
	    url = urljoin(self.url, url)
	    (status, headers, body) = httpc.get_(url, ok=[500, 501,300, 301, 503, 200, 404, 405])        
	    f = open(self.filename, 'wb')
	    f.write(body)
	    f.close()
	return self.readFile(self.filename)

    def readFile(self, filename):
	data = []
	import xlrd
	wb = xlrd.open_workbook(filename)
	sh = wb.sheet_by_index(0)
	for i in range(2, sh.nrows):
	    rec = {}
	    item = sh.row(i)
	    for n in range(0, len(self.fields)):
#		print (item[n])
		rec[self.fields[n]] = item[n].value
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
#	objects = self.parse(self.get(self.url))
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
    ex = RoskaznaTerorgansExtractor()
    ex.process()
	
	
    