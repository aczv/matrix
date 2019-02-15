import datetime
from django.db import models

import matrix.core.constants as constants
from matrix.core.models import Contact

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
    url = models.URLField(blank=True)

    environment = models.CharField(
        max_length=30, default=constants.ENVIRONMENT_PRODUCTION,
        choices=constants.ENVIRONMENT_CHOICES,
    )

    comment = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
