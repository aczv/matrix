from django.contrib import admin

from .models import AppServer
# , SqlServer, Database
from .models import Project, Program, Deployment

# ==============================================================================
# Servers & Databases
# ==============================================================================

@admin.register(AppServer)
class AppServerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ip_address', 'domain_name', 'comment']
    list_display = ['name', 'ip_address', 'domain_name', 'comment']

# @admin.register(SqlServer)
# class SqlServerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'ip_address', 'comment']

# @admin.register(Database)
# class DatabaseAdmin(admin.ModelAdmin):
#     list_display = ['name', 'sql_server', 'comment']
#     save_as = True

# ==============================================================================
# ProgramAdmin
# ==============================================================================

class DeploymentInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    model = Deployment
    fields = ['name', 'url', 'environment', 'country', 'comment']
    classes = ['collapse']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ['name', 'comment']
    list_display = ['name', 'project', 'contact', 'comment']
    list_filter = ['project', 'contact']
    inlines = [DeploymentInline]

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'url']
    list_display = ['name', 'program', 'environment', 'country', 'url', 'get_project', 'get_app_server_name', 'comment']
    list_display_links = ['name']
    list_filter = ['program__project', 'environment', 'country', 'app_server', 'program']
    autocomplete_fields = ['program']
    save_as = True

    def get_project(self, obj):
        return obj.program.project
    get_project.short_description = 'Project'
    get_project.admin_order_field = 'program__project'

    def get_app_server_name(self, obj):
        # ??? use global -
        return obj.app_server.name if obj.app_server is not None else "-"
    get_app_server_name.short_description = 'App server'
    get_app_server_name.admin_order_field = 'app_server__name'

# ==============================================================================
# ProjectAdmin
# ==============================================================================

class ProgramInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    model = Program
    fields = ['name', 'contact', 'comment']
    classes = ['collapse']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'contact']
    inlines = [ProgramInline]
