from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RECRUITER = "RECRUITER", "Recruiter"
        APPLICANT = "APPLICANT", "Applicant"
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.APPLICANT)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    profile_picture = models.ImageField(upload_to="profile_photos/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

    
class ApplicantUser(User):
    class Meta:
        proxy = True # Why proxy = True is the key line: it tells Django "don't create a new database table for this — just give me a different Python-level view of the existing User table."
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

class RecruiterUser(User):
    class Meta:
        proxy = True
        verbose_name = "Recruiter"
        verbose_name_plural = "Recruiters"

class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"