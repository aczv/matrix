from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Project
from .tables import ProjectTable

def projects(request):
    table = ProjectTable(Project.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'software/projects.html', {'table': table})
