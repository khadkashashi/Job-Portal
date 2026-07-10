from django.urls import path

from . import views

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply-job" ),
    path("my-applications/", views.my_applications,name="my-applications"),
    path("applications/", views.application_list, name="application-list"),
    path("applications/<int:pk>/",views.application_detail,name="application-detail" ),

]