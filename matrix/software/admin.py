from django.contrib import admin

from .models import AppServer, SqlServer, Database
from .models import Project, Program, Deployment

# ==============================================================================
# Servers & Databases
# ==============================================================================

@admin.register(AppServer)
class AppServerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ip_address', 'domain_name', 'comment']
    list_display = ['name', 'ip_address', 'domain_name', 'comment', 'get_deployment_count']

    def get_deployment_count(self, obj):
        return obj.deployment_set.count()
    get_deployment_count.short_description = 'Deployments'

@admin.register(SqlServer)
class SqlServerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ip_address', 'domain_name', 'comment']
    list_display = ['name', 'ip_address', 'domain_name', 'comment']

@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'sql_server', 'comment']

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
    list_display = ['name', 'project', 'contact', 'comment', 'get_deployment_count']
    list_filter = ['project', 'contact']
    inlines = [DeploymentInline]

    def get_deployment_count(self, obj):
        return obj.deployment_set.count()
    get_deployment_count.short_description = 'Deployments'

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'url']
    list_display = ['name', 'program', 'environment', 'country', 'url', 'get_project', 'get_appserver', 'comment']
    list_display_links = ['name']
    list_filter = ['program__project', 'environment', 'country', 'app_server', 'program']
    autocomplete_fields = ['program', 'app_server']
    save_as = True

    def get_project(self, obj):
        return obj.program.project
    get_project.short_description = 'Project'
    get_project.admin_order_field = 'program__project'

    def get_appserver(self, obj):
        return obj.app_server
    get_appserver.short_description = 'App server'
    get_appserver.admin_order_field = 'app_server__name'

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
    list_display = ['name', 'contact', 'get_program_count']
    inlines = [ProgramInline]

    def get_program_count(self, obj):
        return obj.program_set.count()
    get_program_count.short_description = 'Programs'
