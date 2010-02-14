#-*- coding: utf-8 -*-
"""
OpenGovData.ru Models

by Ivan Begtin (c) 2009
"""
import datetime, traceback

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

LANG_RU = u'RU'
LANG_EN = u'EN'

LANGUAGES_CHOICES = (
	(LANG_RU, _('Russian')),
	(LANG_EN, _('English')),
)


class OrganizationType(models.Model):
    """Organization type"""
    name = models.CharField(name=_('name'), max_length=50)

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Organization type')
	verbose_name_plural = _('Organization types')
	


class Tag(models.Model):
    """Tag model"""
    name = models.CharField(name=_('name'), max_length=50)

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Tag')
	verbose_name_plural = _('Tags')
	
	

class Organization(models.Model):
    """Organization"""
    name = models.CharField(name=_('name'), max_length=200)
    description = models.TextField(name=_('description'), blank=True, null=True)
    website = models.URLField(name=_('website'), max_length=500, blank=True, null=True)
    address = models.TextField(name=_("address"), max_length=500, blank=True, null=True)
    

    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Organization')
	verbose_name_plural = _('Organizations')


class DataFormat(models.Model):
    """Data format"""
    name = models.CharField(name=_('name'), max_length=200)
	
    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Data format')
	verbose_name_plural = _('Data formats')

class DataType(models.Model):
    """Data type"""
    name = models.CharField(name=_('name'), max_length=200)
	
    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('Source Data type')
	verbose_name_plural = _('Source Data types')



class DataSource(models.Model):
    """Data source"""
    name = models.CharField(_('name'), max_length=500)
    slug = models.CharField(_('slug'), unique=True, max_length=50)
    about_txt = models.TextField(_('about txt'), blank=True, null=True)
    language = models.CharField(_('language'), max_length=10, default=LANG_RU, choices=LANGUAGES_CHOICES)
    description_link = models.URLField(_('description link'), max_length=500, blank=True, null=True)
    permanent_link = models.URLField(_('permanent link'), max_length=500, blank=True, null=True)    
    
    organization = models.ForeignKey(Organization, null=True, blank=True)
    datatype = models.ManyToManyField(DataType, blank=True, null=True)
    formats = models.ManyToManyField(DataFormat, blank=True, null=True)
    
    copyright_txt = models.TextField(_('Copyright'), blank=True, null=True)    
    
    date_created = models.DateTimeField(_('date created'), default=datetime.datetime.now())
    date_updated = models.DateTimeField(_('date updated'), default=datetime.datetime.now())


    def tags(self):
	return DataSourceTag.objects.filter(source=self)

    def __unicode__(self):
	return u'%s %s' %(self.name, self.description_link)

    class Meta:
	verbose_name = _('Data source')
	verbose_name_plural = _('Data sources')


class DataSourceTag(models.Model):
    """Data source tag"""
    tag = models.ForeignKey(Tag)
    source = models.ForeignKey(DataSource)

    def __unicode__(self):
	return u'%s: %s' %(self.source.name, self.tag.name)

    class Meta:
	unique_together = ['tag', 'source']
	verbose_name = _('Data source tag')
	verbose_name_plural = _('Data source tags')


    
class FieldType(models.Model):
    """Data field type"""    
    name = models.CharField(name=_('name'), max_length=200, unique=True)
    level = models.IntegerField(name=_('level'), default=0)
    min_length = models.IntegerField(name=_('Min length'), blank=True, null=True, default=None)
    max_length = models.IntegerField(name=_('Max length'), blank=True, null=True, default=None)
    parent = models.ForeignKey('self', null=True, blank=True)
	
    def __unicode__(self):
	return self.name
	
    class Meta:
	verbose_name = _('Field type')
	verbose_name_plural = _('Field types')
    


class OpenDataType(models.Model):
    """Open Data type"""
    key = models.CharField(name=_('key'), max_length=50, unique=True)
    name = models.CharField(name=_('name'), max_length=200, blank=True, null=True)
    description = models.TextField(name=_('description'),  blank=True, null=True)
	
    def __unicode__(self):
	return u'%s' %(self.name)

    class Meta:
	verbose_name = _('OpenData type')
	verbose_name_plural = _('OpenData types')


class OpenData(models.Model):
    """OpenData model"""
    slug = models.CharField(_('slug'), unique=True, max_length=50)
    name = models.CharField(_('name'), max_length=500)
    description = models.TextField(_('description'), blank=True, null=True)
    language = models.CharField(_('language'), max_length=10, default="ru", choices=LANGUAGES_CHOICES)
    opendata_id = models.CharField(name=_('opendata id'), unique=True, max_length=100)
    opendata_url = models.URLField(name=_('opendata url'), max_length=500, blank=True, null=True)
    location_url = models.URLField(name=_('location url'), max_length=500, blank=True, null=True)
    
    spec_id = models.CharField(name=_('spec id'), unique=True, max_length=100)
    
    dinfo_isupdatable = models.BooleanField(name=_('is updatable'), default=False)
    date_created = models.DateTimeField(_('date created'), default=datetime.datetime.now())
    date_updated = models.DateTimeField(_('date updated'), default=datetime.datetime.now())
    author_name = models.CharField(name=_('author name'), max_length=200, blank=True, null=True)
    author_website = models.URLField(name=_('author website'), max_length=200, blank=True, null=True)
    
    organization = models.ForeignKey(Organization, null=True, blank=True)
    datasource = models.ForeignKey(DataSource, blank=True, null=True)        

    datatypes = models.ManyToManyField(OpenDataType, blank=True, null=True)
    formats = models.ManyToManyField(DataFormat, blank=True, null=True)

        
    def fields(self):
	return DataField.objects.filter(opendata=self).order_by('num')

    def tags(self):
	return OpenDataTag.objects.filter(opendata=self)
	
    def files(self):
	return OpenDataFile.objects.filter(opendata=self)

    def __unicode__(self):
	return u'%s' %(self.opendata_id)

    class Meta:
	verbose_name = _('OpenData dataset')
	verbose_name_plural = _('OpenData datasets')

class OpenDataTag(models.Model):
    """Data source tag"""
    tag = models.ForeignKey(Tag)
    opendata = models.ForeignKey(OpenData)

    def __unicode__(self):
	return u'%s: %s' %(self.opendata.name, self.tag.name)

    class Meta:
	unique_together = ['tag', 'opendata']
	verbose_name = _('Opendata tag')
	verbose_name_plural = _('Opendata tags')

class OpenDataFile(models.Model):
    """Open data published file"""
    urlpath = models.URLField(_('URL path'), max_length=255)
    opendata = models.ForeignKey(OpenData)
    specid = models.CharField(_('Spec id'), max_length=50)
    filepath = models.CharField(_('File path'), max_length=500, blank=True, null=True)
    format = models.ForeignKey(DataFormat)
    datatype = models.ForeignKey(OpenDataType)
    hash_sha512 = models.CharField(_('SHA512 Hash'), max_length=150, blank=True, null=True)
    date_updated = models.DateTimeField(_('date updated'), default=datetime.datetime.now())
    
    def __unicode__(self):
	return self.urlpath
	
    class Meta:
	verbose_name = _('Open data file')
	verbose_name_plural = _('Open data files')

class DataField(models.Model):
    """Data Field"""
    opendata = models.ForeignKey(OpenData)
    key = models.CharField(name=_('key'), max_length=200)
    num = models.IntegerField(name=_('num'))
    is_unique = models.BooleanField(name=_('is_unique'), default=False)
    name = models.CharField(name=_('name'), max_length=200)
    description = models.TextField(name=_('description'), blank=True, null=True)
    field_type = models.ForeignKey(FieldType)
    units = models.CharField(name=_('units'), max_length=200, null=True, blank=True)
    
    def __unicode__(self):
	return self.name
	
    class Meta:
	verbose_name = _('Data field')
	verbose_name_plural = _('Data fields')
	


