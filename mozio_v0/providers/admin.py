from django.contrib import admin

from .models import Provider, ServiceArea


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'language', 'currency']


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ['polygon_name', 'price']
