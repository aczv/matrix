from django.contrib import admin

from .models import Branch, Department, Responsible, Cloth, Reservation


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    pass


@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    search_fields = ['branch']
    list_filter = ['branch', 'size', 'confirmed']
    list_display = ['branch', 'cloth', 'quantity', 'size', 'confirmed']
    list_display_links = ['branch', 'cloth']
