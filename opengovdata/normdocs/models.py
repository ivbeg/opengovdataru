#-*- coding: utf-8 -*-
"""
OpenGovData.ru Models NormDocs

by Ivan Begtin (c) 2009
"""
import datetime, traceback

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

DOCUMENT_FORMATS = [
    (u'DOC', _('Microsoft Word')),
    (u'PDF', _('Adobe PDF')),
    (u'XLS', _('Microsoft Excel')),
    (u'RTF', _('Microsoft RTF')),
    (u'TIF', _('TIFF')),
]

class Tag(models.Model):
    """Tag model"""
    name = models.CharField(name=_('name'), max_length=50)
    
    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Tag')
	verbose_name_plural = _('Tags')


class DocumentType(models.Model):
    """Document type"""
    name = models.CharField(name=_('name'), max_length=50, unique=True)

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Document type')
	verbose_name_plural = _('Document type')


class OrganizationLevel(models.Model):
    """Organization level"""
    name = models.CharField(name=_('name'), max_length=50, unique=True)

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Organization level')
	verbose_name_plural = _('Organization level')

class Organization(models.Model):
    """Organization"""
    name = models.CharField(name=_('name'), max_length=200, unique=True)
    description = models.TextField(name=_('description'), null=True, blank=True)
    website = models.CharField(name=_('website'), max_length=500, null=True, blank=True)
    address = models.TextField(name=_('address'), null=True, blank=True)
    orglevel = models.ForeignKey(OrganizationLevel)

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Organization')
	verbose_name_plural = _('Organization')


class DocumentTheme(models.Model):
    """Document themes"""
    name = models.CharField(name=_('name'), max_length=50)

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Document theme')
	verbose_name_plural = _('Document themes')
    

class Document(models.Model):
    """Law document"""
    name = models.CharField(name=_('name'), max_length=255)
    description = models.TextField(name=_('description'))
    file = models.FileField(upload_to='files/laws')
    url = models.URLField(name=_('document url'), max_length=500, blank=True, null=True)

    format = models.CharField(name=_('doc format'), max_length=50, choices=DOCUMENT_FORMATS, default=u'DOC')
    
    theme = models.ForeignKey(DocumentTheme)
    doctype = models.ForeignKey(DocumentType)    
    organization = models.ForeignKey(Organization)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    taglist = models.CharField(name=_('taglist'), max_length=200, blank=True, null=True, help_text=u'Список тэгов через запятую')
    
    date_published = models.DateField(name=_('date published'), null=True, blank=True)
    date_created = models.DateTimeField(name=_('date created'), default=datetime.datetime.now())

    def save(self, force_insert=False, force_update=False):
	super(Document, self).save(force_insert, force_update) # Call the "real" save() method.
	parts = self.taglist.split(',')
	if len(parts) > 1 and len(parts[0].strip()) > 0:
	    self.tags.all().delete()
	    for part in parts:
		part = part.strip()
		tag, created = Tag.objects.get_or_create(name=part)
		if created:
		    tag.save()
		self.tags.add(tag)			
        	

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Document')
	verbose_name_plural = _('Documents')
	
	
