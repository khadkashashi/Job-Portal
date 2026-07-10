from django.urls import path
from . import views
from .views import PublicJobListView
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("jobs/", PublicJobListView.as_view(), name="job-list"),

]