from django.urls import path
from . import views
from .views import PublicJobListView
urlpatterns = [
    path("", views.home, name="home"),
    path("jobs/", PublicJobListView.as_view(), name="job-list"),

]