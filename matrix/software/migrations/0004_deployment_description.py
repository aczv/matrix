# Generated by Django 2.1.4 on 2019-02-15 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0003_auto_20190215_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]