from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Country, Contact

admin.site.register(User, UserAdmin)
# admin.site.unregister(auth.models.Group)

admin.site.site_header = "Matrix Admin"
admin.site.site_title = "Matrix Admin Portal"
admin.site.index_title = "Welcome to Matrix Researcher Portal"

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'alpha2', 'alpha3']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
