from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_by')
    search_fields = ('name', 'email', 'skills', 'education')
