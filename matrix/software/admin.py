from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext as _
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
    """Decorator used for rendering a link to the list display of
    a related model in the admin detail page.
    attr (str):
        Name of the related field.
    short_description (str):
        Field display name.
    empty_description (str):
        Value to display if the related field is None.
    query_string (function):
        Optional callback for adding a query string to the link.
        Receives the object and should return a query string.
    The wrapped method receives the related object and
    should return the link text.
    Usage:
        @admin_changelist_link('credit_card', _('Credit Card'))
        def credit_card_link(self, credit_card):
            return credit_card.name
    """
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
                func(self, related_obj)
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
        'comment',
        'get_deployment_count',
        'deployments_link',
    )
    list_select_related = ['country']

    def get_deployment_count(self, obj):
        return obj.deployment_set.count()
    get_deployment_count.short_description = 'Deployments'

    @admin_changelist_link(
        'deployment_set',
        _('Deployments'),
        query_string=lambda c: 'app_server__id__exact={}'.format(c.pk)
    )
    def deployments_link(self, deployments):
        return _('Deployments')

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
    list_display = ['name', 'project', 'contact', 'comment', 'get_deployment_count', 'get_deployments_url']
    list_filter = ['project', 'contact']
    inlines = [DeploymentInline]

    def get_deployment_count(self, obj):
        return obj.deployment_set.count()
    get_deployment_count.short_description = 'Deployments'

    def get_deployments_url(self, obj):
        return reverse('admin:software_deployment_changelist', kwargs={'program__id__exact': obj.pk})

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    # search_fields = ['name', 'url']
    list_display = ['name', 'program', 'environment', 'country', 'url', 'get_appserver', 'comment']
    list_display_links = ['name']
    list_select_related = ['program', 'country', 'app_server']
    list_filter = ['program__project', 'environment', 'country', 'app_server', 'program']
    autocomplete_fields = ['program', 'app_server']
    save_as = True

    def get_appserver(self, obj):
        return obj.app_server
    get_appserver.short_description = 'App server'
    # get_appserver.admin_order_field = 'app_server__name'

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
