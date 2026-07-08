from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_job, name="create-job"),
    
    path("create/", views.create_job, name="create-job"),
    path("my-jobs/", views.my_jobs, name="my-jobs"),

]