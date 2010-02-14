from django.contrib import admin
from djlinks.models import *

class LinkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'icon_path', 'linkorder')
    search_fields = ['name', 'slug']


class WebLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'description', 'linkorder', 'icon_path', 'thumb_path', 'date_created', 'date_modified')
    list_filter = ['category']
    search_fields = ['title', 'url']

class FeedAdmin(admin.ModelAdmin):
    list_display = ('feed_url', 'weblink', 'name', 'shortname', 'title')
    search_fields = ['name', 'title', 'feed_url']

class GlossaryItemAdmin(admin.ModelAdmin):
    list_display = ('slug', 'topic', 'name', 'text', 'date_created')
    search_fields = ['slug', 'name', 'text']

class GlossaryTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ['name',]


admin.site.register(GlossaryTopic, GlossaryTopicAdmin)
admin.site.register(GlossaryItem, GlossaryItemAdmin)
admin.site.register(WebLink, WebLinkAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(LinkCategory, LinkCategoryAdmin)
admin.site.register(NewsEntry)
admin.site.register(NewsChannel)
        