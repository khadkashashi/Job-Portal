from django.urls import path
from . import views
from .views import PublicJobListView

urlpatterns = [
    path("create/", views.create_job, name="create-job"),
    path("my-jobs/", views.my_jobs, name="my-jobs"),
    path("<int:pk>/", views.job_detail, name="job-detail"),
    path("jobs/", PublicJobListView.as_view(), name="job-list"),
    path("delete/<int:pk>/", views.delete_job, name="delete-job"),
    path("edit/<int:pk>/", views.edit_job, name="edit-job"),

]