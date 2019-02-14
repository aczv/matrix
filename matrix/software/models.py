import datetime
from django.db import models

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
    website_url = models.URLField(blank=True)
    api_url = models.URLField(blank=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
