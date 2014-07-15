from django.contrib import admin

from home.models import BlogEntry


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_date', 'entry_subject']

admin.site.register(BlogEntry, BlogEntryAdmin)
