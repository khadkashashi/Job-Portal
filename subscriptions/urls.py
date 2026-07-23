from django.urls import path
from . import views

urlpatterns = [
    path("choose/", views.choose_plan, name="choose-plan"),
    path("pay/<int:plan_id>/", views.start_payment, name="start-payment"),
    path("callback/", views.payment_callback, name="payment-callback"),
]