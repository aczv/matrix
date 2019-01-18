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
