from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_company, name="create-company"),
    path("profile/", views.company_profile, name="company-profile"),
    path("<slug:slug>/", views.company_detail, name="company-detail"),
    path("<slug:slug>/edit/", views.edit_company, name="edit-company"),
    path("companies/", views.company_list, name="company-list"),
]