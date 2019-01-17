from django.contrib import admin

from .models import Server, Site


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


# Matrix common settings

from django.contrib import admin

admin.site.site_header = "Matrix Admin"
admin.site.site_title = "Matrix Admin Portal"
admin.site.index_title = "Welcome to Matrix Researcher Portal"
