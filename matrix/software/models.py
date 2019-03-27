import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

import matrix.core.constants as constants
from matrix.core.models import Country, Contact

# ==============================================================================
# Servers & Databases
# ==============================================================================

class ServerBase(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)
    domain_name = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return "{} ({})".format(self.name, self.ip_address)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.domain_name = self.domain_name.lower()
        super().save(*args, **kwargs)

class AppServer(ServerBase):
    pass

class SqlServer(ServerBase):
    pass

class Database(models.Model):
    name = models.CharField(max_length=100)
    sql_server = models.ForeignKey(SqlServer, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['sql_server', 'name']

    def __str__(self):
        return "{} ({})".format(self.name, self.sql_server.name)

# ==============================================================================
# Programs & Deployments
# ==============================================================================

class Project(models.Model):
    name = models.CharField(max_length=100)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Program(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Deployment(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    environment = models.CharField(
        max_length=30, default=constants.ENVIRONMENT_PRODUCTION,
        choices=constants.ENVIRONMENT_CHOICES,
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    url = models.URLField(blank=True)
    app_server = models.ForeignKey(AppServer, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Designates whether the deployment is active.'),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['program', 'environment', 'country', 'pk']
