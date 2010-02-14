from normdocs.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
    
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'description', 'orglevel', 'address')
    list_filter = ['orglevel',]
    search_fields = ['name', 'website', 'description']

class OrganizationLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class DocumentThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'theme', 'format', 'doctype', 'organization', 'taglist', 'date_published', 'date_created')
    list_filter = ['format', 'theme', 'doctype', 'organization', 'tags']
    search_fields = ['name', 'description']


admin.site.register(Tag, TagAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationLevel, OrganizationLevelAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(DocumentTheme, DocumentThemeAdmin)
admin.site.register(Document, DocumentAdmin)
