from django.contrib import admin
from .models import Company

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "owner", "city", "country", "created_at")
    search_fields = ("company_name", "owner__username", "email")
    list_filter = ("country",)