from django.contrib import admin
from .models import UserDetails, Competencies, MeasurableResults, Resume, ResumeDetails

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    pass

@admin.register(Competencies)
class CompetenciesAdmin(admin.ModelAdmin):
    pass

@admin.register(MeasurableResults)
class MeasurableResultsAdmin(admin.ModelAdmin):
    pass

@admin.register(ResumeDetails)
class ResumeDetailsAdmin(admin.ModelAdmin):
    pass