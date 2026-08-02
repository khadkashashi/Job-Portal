from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser, ApplicantUser, RecruiterUser, User

# Register your models here.
class ApplicantAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="APPLICANT")

    def save_model(self, request, obj, form, change):
        obj.role = "APPLICANT"
        super().save_model(request, obj, form, change)


class RecruiterAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="RECRUITER")

    def save_model(self, request, obj, form, change):
        obj.role = "RECRUITER"
        super().save_model(request, obj, form, change)


class AdminUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="ADMIN")

    def save_model(self, request, obj, form, change):
        obj.role = "ADMIN"
        super().save_model(request, obj, form, change)

admin.site.register(User,UserAdmin)
admin.site.register(ApplicantUser, ApplicantAdmin)
admin.site.register(RecruiterUser, RecruiterAdmin)
admin.site.register(AdminUser, AdminUserAdmin)


#Why get_queryset is overridden, not a new field or table: each proxy model shows the exact same data, just pre-filtered by role — so "Applicants" in the admin sidebar only lists users where role="APPLICANT", "Recruiters" only role="RECRUITER", etc. Editing a user through any of these three lists edits the same real row in the same real User table — there's no duplication or sync risk.
#Why this needs to happen in save_model, not just as a form default: save_model runs right before Django actually writes to the database, on both create and edit — so it guarantees the role is correct regardless of whether the role field appears on the form at all, and it can't be second-guessed by whatever the form's fields happen to include.