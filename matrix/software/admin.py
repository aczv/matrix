from django.contrib import admin

from .models import Project, Program, Deployment

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
    list_display = ['name', 'program', 'environment', 'country', 'url', 'get_project', 'comment']
    list_display_links = ['name']
    list_filter = ['program__project', 'environment', 'country', 'program']
    autocomplete_fields = ['program']
    save_as = True

    def get_project(self, obj):
        return obj.program.project
    get_project.short_description = 'Project'
    get_project.admin_order_field = 'program__project'

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
