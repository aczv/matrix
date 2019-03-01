from django.shortcuts import render
from .models import Project

def projects(request):
    return render(request, 'software/projects.html', {'projects': Project.objects.all()})
