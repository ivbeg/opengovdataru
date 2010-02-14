# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _


# Create your models here.

ICON_PATH = u'/static/20/images/'
ICON_NAME_MAP = (
    (ICON_PATH + u'bullet_black.png', (u'Default')),
    (ICON_PATH + u'folder_go.png', (u'Category')),
    (ICON_PATH + u'flags/ru.png', (u'Russian flag')),
    (ICON_PATH + u'special/igz.png', (u'IGZ')),
)


class GlossaryTopic(models.Model):
    name = models.CharField(_("name"), max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True)

    class Admin:
	list_display = ('name', 'parent')
	search_fields = ('name')
    
    class Meta:
	verbose_name = _("Glossary topic")
	verbose_name_plural = _("Glossary topics")
	
    def __unicode__(self):
	return self.name


class GlossaryItem(models.Model):
    """Элемент словаря (справочника)"""
    slug = models.CharField(_("slug"), max_length=20)
    name = models.CharField(_("name"), max_length=100)
    topic = models.ForeignKey('self', null=True, blank=True)
    text = models.TextField(_("text"), blank=True)
    related = models.ManyToManyField('self', verbose_name="Related items", blank=True, null=True)

    date_created = models.DateTimeField(_("date created"), default=datetime.datetime.now())

    class Admin:
	list_display = ('slug', 'name', 'text')
	search_fields = ('slug', 'name', 'text')
    
    class Meta:
	verbose_name = _("Glossary item")
	verbose_name_plural = _("Glossary items")
	
    def __unicode__(self):
	return self.name



class Advice(models.Model):
    """Советы пользователям"""
    title  = models.CharField(_("title"), max_length=500, blank=True)
    body = models.TextField(_("body"), blank=True)
    modified_date = models.DateTimeField(_("date modified"), default=datetime.datetime.now())
    
    
    class Admin:
	list_display = ('modified_date', 'title', 'body')
	search_fields = ('title', 'body')
    
    class Meta:
	verbose_name = _("Advice")
	verbose_name_plural = _("Advices")
	
    def __unicode__(self):
	return self.title

class NewsChannel(models.Model):
    """Новостной канал"""
    code = models.CharField(_("code"), max_length=10)
    title = models.CharField(_("title"), max_length=500)

    class Admin:
	list_display = ('code', 'title')
	search_fields = ('title')

    class Meta:
	verbose_name = _("News channel")
	verbose_name_plural = _("News channels")

    def get_news(self, limit=20):
	if limit is None:
	    limit = 50
	return NewsEntry.objects.filter(channels__id__in=[self.id])[:limit]
	
    def __unicode__(self):
	return self.title
    


class NewsEntry(models.Model):
    """Новость в упрощённом формате. Заголовок, тело, дата публикации"""
    title = models.CharField(_("title"), max_length=500, blank=True)
    body = models.TextField(_("News body"), blank=True)
    pubdate = models.DateTimeField(_("date published"), default=datetime.datetime.now())
    source = models.URLField(_('source'), blank=True, null=True)
    channels = models.ManyToManyField(NewsChannel, verbose_name="News channels")
    
    class Admin:
	list_display = ('pubdate', 'title', 'body', 'source')
	search_fields = ('title', 'body')
	js = ['tiny_mce/tiny_mce.js', 'js/textareas.js']    

    class Meta:
	verbose_name = _("News")
	verbose_name_plural = _("News items")
	
    def __unicode__(self):
	return self.title



class LinkCategory(models.Model):
    """Категория ссылки"""
    name = models.CharField(_("category name"), max_length=500, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    icon_path = models.CharField(_('icon'), max_length=200, choices=ICON_NAME_MAP, default=ICON_PATH + u'folder_go.png')
    slug = models.CharField(_("slug"), max_length=100, blank=True)
    linkorder = models.IntegerField(_('order number'), default=100)


    class Admin:
        list_display = ['slug', 'name','linkorder', 'parent']

    class Meta:
        verbose_name = _('Link category')
        verbose_name_plural = _('Link categories')
	
    def get_links_list(self):
        return WebLink.objects.filter(category=self).order_by('-linkorder')

    def __unicode__(self):
        return self.name


    def get_children(self):
        children = []
        return LinkCategory.objects.filter(parent=self)
    

    def get_children_codes(self, item=None):
        if not item:
            item = self
        children = []
        objects = LinkCategory.objects.filter(parent=item)
        if len(objects) > 0:
            for obj in objects:
                children.append(obj.id)
                children.extend(self.get_children_codes(obj))
        return children

    def get_parent_codes(self): 
        codes = []
        codes_sort = []
        current = self
        while current:
            codes.append(current)
            current = current.parent
        for i in range(len(codes)-1 , -1, -1):
           codes_sort.append(codes[i])
        return codes_sort

class WebLink(models.Model):
    """Ссылка на веб сайт"""
    title = models.CharField(_("url name"), max_length=500, blank=True)
    url	=  models.URLField(_("url"), blank=True, verify_exists=False)    
    description = models.TextField(_('description'), blank=True)
    category = models.ManyToManyField(LinkCategory, null=True)
    linkorder = models.IntegerField(_('order number'), default=100)
    icon_path = models.CharField(_('icon'), max_length=200, choices=ICON_NAME_MAP, default=ICON_PATH + u'bullet_black.png')
    thumb_path = models.CharField(_('thumb'), max_length=200, null=True, blank=True)
    
    date_created = models.DateTimeField(_('creation date'), default=datetime.datetime.now())
    date_modified = models.DateTimeField(_('modification date'), auto_now=True)
    
    class Admin:
        list_display = ['title','url', 'linkorder', 'description']
        list_filter = ('category',)
        search_fields = ['title','url']
	
    class Meta:
        verbose_name = _('Weblink')
        verbose_name_plural = _('Weblinks')
    

    def __unicode__(self):
        return u'%s (%s)'%(self.title, self.url)


    def get_feeds(self):       
        return Feed.objects.filter(weblink=self)

    def has_feeds(self):
        return (Feed.objects.filter(weblink=self).count() > 0)


class Feed(models.Model):
    feed_url = models.URLField(_('feed url'), unique=True)
    weblink = models.ForeignKey(WebLink, null=True)

    name = models.CharField(_('name'), max_length=100)
    shortname = models.CharField(_('shortname'), max_length=50)
    is_active = models.BooleanField(_('is active'), default=True, \
      help_text=_('If disabled, this feed will not be further updated.') )

    title = models.CharField(_('title'), max_length=200, blank=True)
    tagline = models.TextField(_('tagline'), blank=True)
    link = models.URLField(_('link'), blank=True)

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField(_('etag'), max_length=50, blank=True)
    last_modified = models.DateTimeField(_('last modified'), null=True, blank=True)
    last_checked = models.DateTimeField(_('last checked'), null=True, blank=True)

    class Admin:
        list_display = ('name', 'feed_url', 'title', 'last_modified', \
          'is_active')
        fields = (
          (None, {'fields':('feed_url', 'name', 'shortname', 'is_active')}),
          (_('Fields updated automatically by Feedjack'), {
            'classes':'collapse',
            'fields':('title', 'tagline', 'link', 'etag', 'last_modified', \
              'last_checked')})
        )
        search_fields = ['feed_url', 'name', 'title']

    class Meta:
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')
        ordering = ('name', 'feed_url',)

    def __str__(self):
        return '%s (%s)' % (self.name, self.feed_url)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.feed_url)

    def save(self):
        super(Feed, self).save()    
