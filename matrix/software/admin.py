from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import AppServer, SqlServer, Database
from .models import Project, Program, Deployment

def admin_changelist_url(model):
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    return reverse('admin:{}_{}_changelist'.format(
        app_label,
        model_name)
    )
def admin_changelist_link(
    attr,
    short_description,
    empty_description="-",
    query_string=None
):
    def wrap(func):
        def field_func(self, obj):
            related_obj = getattr(obj, attr)
            if related_obj is None:
                return empty_description
            url = admin_changelist_url(related_obj.model)
            if query_string:
                url += '?' + query_string(obj)
            return format_html(
                '<a href="{}">{}</a>',
                url,
                func(self, obj, related_obj)
            )
        field_func.short_description = short_description
        field_func.allow_tags = True
        return field_func
    return wrap

# ==============================================================================
# Servers & Databases
# ==============================================================================

@admin.register(AppServer)
class AppServerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ip_address', 'domain_name', 'comment']
    list_display = (
        'name',
        'ip_address',
        'domain_name',
        'country',
        'deployments_link',
        'comment',
    )
    list_select_related = ['country']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _deployment_count=Count("deployment", distinct=True),
        )
        return queryset

    @admin_changelist_link(
        'deployment_set',
        'Deployments',
        query_string=lambda c: 'app_server__id__exact={}'.format(c.pk)
    )
    def deployments_link(self, obj, related_obj):
        return obj._deployment_count

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
    list_display = (
        'name',
        'project',
        'contact',
        'deployments_link',
        'comment',
    )
    list_select_related = ['project', 'contact']
    list_filter = ['project', 'contact']
    inlines = [DeploymentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _deployment_count=Count("deployment", distinct=True),
        )
        return queryset

    @admin_changelist_link(
        'deployment_set',
        'Deployments',
        query_string=lambda c: 'program__id__exact={}'.format(c.pk)
    )
    def deployments_link(self, obj, related_obj):
        return obj._deployment_count

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'url']
    list_display = ['name', 'program', 'environment', 'country', 'url', 'app_server', 'comment']
    list_display_links = ['name']
    list_select_related = ['program', 'country', 'app_server']
    list_filter = ['program__project', 'environment', 'country', 'app_server', 'program']
    autocomplete_fields = ['program', 'app_server']
    save_as = True

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
