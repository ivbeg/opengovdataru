import sys, os
import chardet
from eventlet import httpc
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

from opendata.sources.common import *


class FavtAeroportExtractor(OpenDataExtractor):
    fields = ['num', 'registryNumber', 'certNumber', 'certDateFrom', 'certDateTo', 'name', 'location']
    url = 'http://www.favt.ru/ap/ap_rga/'
    
    def __init__(self):
	pass
	
    def get(self, url):
        (status, headers, body) = httpc.get_(url, ok=[500, 501,300, 301, 503, 200, 404, 405])
	return body
    
    def parse(self, data):	    
	d = chardet.detect(data)
	if d.has_key('encoding'):
	    encoding = d['encoding']
	else:
	    encoding = 'utf-8'
	print data
	soup = BeautifulStoneSoup(data, fromEncoding=encoding)
	print soup
	pass
	
    def process(self):
	objects = self.parse(self.get(self.url))
	pass
	
if __name__ == "__main__":
    ex = FavtAeroportExtractor()
    ex.process()
	
	
    