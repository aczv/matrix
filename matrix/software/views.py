from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Project, Deployment
from .tables import ProjectTable, DeploymentTable

def projects(request):
    table = ProjectTable(Project.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'software/projects.html', {'table': table})

def deployments(request):
    table = DeploymentTable(Deployment.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'software/deployments.html', {'table': table})
