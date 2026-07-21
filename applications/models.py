from django.conf import settings
from django.db import models
from jobs.models import Job

class Applicationstatus(models.TextChoices):
    PENDING= "Pending",
    REVIEWING= "Reviewing"
    SHORTLISTED= "Shortlisted",
    REJECTED= "Rejected",
    HIRED= "Hired",

class Application(models.Model):
    applicant = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications" )
    job = models.ForeignKey( Job, on_delete=models.CASCADE,related_name="applications")
    resume = models.FileField( upload_to="resumes/")
    cover_letter = models.TextField( blank=True)
    status = models.CharField( max_length=20,choices=Applicationstatus.choices,default=Applicationstatus.PENDING )
    applied_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    class Meta:
        ordering = ["-applied_at"]
        unique_together = ("applicant", "job")
    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}" #It tells anyone looking at the database exactly who applied for which job at a single glance!

class AIInterview(models.Model):
    application = models.OneToOneField( Application, on_delete=models.CASCADE)
    questions = models.JSONField(default=list, blank=True)
    answers = models.JSONField(default=list, blank=True)
    score = models.IntegerField(default=0)
    feedback = models.TextField(blank=True)
    completed = models.BooleanField(default=False)