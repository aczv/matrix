from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Country(models.Model):
    name = models.CharField(max_length=100)
    alpha2 = models.CharField(max_length=2, unique=True)
    alpha3 = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'countries'

    def save(self, *args, **kwargs):
        self.alpha2 = self.alpha2.upper()
        self.alpha3 = self.alpha3.upper()
        super().save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
