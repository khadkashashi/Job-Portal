from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_company, name="create-company"),
    path("profile/", views.company_profile, name="company-profile"),
]