import django_tables2 as tables
from .models import Project
from .models import Deployment

class ProjectTable(tables.Table):
    class Meta:
        model = Project
        template_name = 'django_tables2/bootstrap.html'

class DeploymentTable(tables.Table):
    class Meta:
        model = Deployment
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('description',)
