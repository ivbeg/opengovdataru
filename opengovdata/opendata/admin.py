from opendata.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

class OpenDataAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'description')
    search_fields = ('slug', 'name', 'description')

class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'description_link', 'about_txt', 'organization')
    list_filter = ['datatype', 'formats', 'organization']
    search_fields = ('slug', 'name', 'about_txt', 'copyright')

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'description')


admin.site.register(OpenData, OpenDataAdmin)
admin.site.register(OpenDataTag)
admin.site.register(OpenDataFile)
admin.site.register(OpenDataType)
admin.site.register(Tag)
admin.site.register(OrganizationType)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(DataType)
admin.site.register(DataFormat)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(DataSourceTag)
admin.site.register(FieldType)
admin.site.register(DataField)
