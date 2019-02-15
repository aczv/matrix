from django.contrib import admin

from .models import Project, Program, Deployment

# ==============================================================================
# ProgramAdmin
# ==============================================================================

class DeploymentInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    model = Deployment
    fields = ['name', 'url', 'comment']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'comment', 'contact']
    list_filter = ['project']
    search_fields = ['name']
    inlines = [DeploymentInline]

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'url', 'comment']
    list_filter = ['program', 'program__project']
    search_fields = ['name', 'url']
    autocomplete_fields = ['program']
    save_as = True

# ==============================================================================
# ProjectAdmin
# ==============================================================================

class ProgramInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    model = Program
    fields = ['name', 'contact']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact']
    search_fields = ['name']
    inlines = [ProgramInline]
