from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
