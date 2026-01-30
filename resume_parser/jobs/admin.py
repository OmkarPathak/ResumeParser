from django.contrib import admin
from .models import Client, Job

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'owner', 'created_at')
    search_fields = ('name', 'email', 'contact_person')
    list_filter = ('owner',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'created_by', 'status', 'created_at')
    list_filter = ('status', 'client', 'created_by')
    search_fields = ('title', 'skills_required')
