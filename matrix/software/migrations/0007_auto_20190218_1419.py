# Generated by Django 2.1.4 on 2019-02-18 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0006_deployment_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deployment',
            options={'ordering': ['program', 'environment', 'country', 'pk']},
        ),
    ]
