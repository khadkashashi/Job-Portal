from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_job, name="create-job"),
    path("my-jobs/", views.my_jobs, name="my-jobs"),
    path("<int:pk>/", views.job_detail, name="job-detail"),
    path("jobs/", views.job_list, name="job-list"),
]