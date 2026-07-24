from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser, ApplicantUser, RecruiterUser, User

# Register your models here.
class ApplicantAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="APPLICANT")

class RecruiterAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="RECRUITER")
    
class AdminUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="ADMIN")

admin.site.register(User,UserAdmin)
admin.site.register(ApplicantUser, ApplicantAdmin)
admin.site.register(RecruiterUser, RecruiterAdmin)
admin.site.register(AdminUser, AdminUserAdmin)


#Why get_queryset is overridden, not a new field or table: each proxy model shows the exact same data, just pre-filtered by role — so "Applicants" in the admin sidebar only lists users where role="APPLICANT", "Recruiters" only role="RECRUITER", etc. Editing a user through any of these three lists edits the same real row in the same real User table — there's no duplication or sync risk.