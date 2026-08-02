from django.contrib import admin
from .models import Job
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "employment_type", "is_active", "deadline", "vacancies")
    list_filter = ("is_active", "employment_type")
    search_fields = ("title", "company__company_name", "location")
    list_editable = ("is_active",)

#Why list_editable = ("is_active",): lets an admin toggle a job active/inactive directly from the list view — no need to open each job individually for a one-field change.