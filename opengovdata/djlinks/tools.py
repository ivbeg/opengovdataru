# -*- coding: utf-8 -*-

"""
Ivan Begtin
tools.py
"""

import feedparser
from django.core.cache import cache

class CachedFeed:
    url = None
    def __init__(self, url, timeout = 7200):
	self.url = url
	self.timeout = timeout
	
    def get_entries(self):
	entries = cache.get('blog_entries')
	if entries:
	    return entries
	else:
	    self.feed = feedparser.parse(self.url)
	    if self.feed: 
		cache.set('blog_entries', self.feed.entries, self.timeout)
    		return self.feed.entries
	    return None

    def get_feed(self):
	return self.feed
    
