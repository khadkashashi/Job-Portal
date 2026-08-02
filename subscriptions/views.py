from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from companies.models import Company
from .khalti import get_payment_url, lookup_khalti_api
from .models import (
    CompanyPlan,
    CompanySubscription,
    Payment,
    PaymentStatus,
    SubscriptionStatus,
    PaymentMethod,
)


def _initiate_khalti_payment(request, company, plan):
    subscription, _created = CompanySubscription.objects.get_or_create(company=company, defaults={"plan": plan})
    subscription.plan = plan
    subscription.status = SubscriptionStatus.PENDING
    subscription.save()
    payment = get_payment_url(
        url=request.build_absolute_uri(reverse("payment-callback")),
        amount=plan.price * 100,  # Khalti wants paisa, not rupees
        purchase_order_id=subscription.id,
        purchase_order_name=f"{company.company_name} - {plan.name}",
        name=company.owner.get_full_name() or company.owner.username,
        email=company.owner.email,
    )

    if payment.get("pidx"):
        Payment.objects.create(
            subscription=subscription,
            payment_method=PaymentMethod.KHALTI,
            pidx=payment["pidx"],
            status=PaymentStatus.PENDING,
            amount=plan.price,
        )
        return payment["payment_url"]
    return None


@login_required
def choose_plan(request):
    if not hasattr(request.user, "company"):
        messages.warning(request, "Please create your company first.")
        return redirect("create-company")
    plans = CompanyPlan.objects.exclude(name="Free")
    return render(request, "subscriptions/choose_plan.html", {"plans": plans})


@login_required
def start_payment(request, plan_id):
    company = request.user.company
    plan = get_object_or_404(CompanyPlan, pk=plan_id)
    payment_url = _initiate_khalti_payment(request, company, plan)
    if payment_url:
        return render(request, "subscriptions/pay.html", {"payment_url": payment_url})
    messages.error(request, "Something went wrong starting the payment. Please try again.")
    return redirect("choose-plan")


def admin_start_payment(request, company_id, plan_id):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        messages.error(request, "You don't have access to do this.")
        return redirect("login")
    company = get_object_or_404(Company, pk=company_id)
    plan = get_object_or_404(CompanyPlan, pk=plan_id)
    payment_url = _initiate_khalti_payment(request, company, plan)
    if payment_url:
        return render(request, "subscriptions/pay.html", {"payment_url": payment_url})
    messages.error(request, "Something went wrong starting the payment. Please try again.")
    return redirect("admin-dashboard")


def payment_callback(request):
    pidx = request.GET.get("pidx")
    if not pidx:
        return HttpResponse("Something went wrong, please contact admin.")
    result = lookup_khalti_api(pidx)
    payment = get_object_or_404(Payment, pidx=pidx)
    subscription = payment.subscription

    if result.get("status") == "Completed":
        payment.status = PaymentStatus.SUCCESS
        payment.transaction_id = request.GET.get("transaction_id", "")
        plan = subscription.plan
        if subscription.status == SubscriptionStatus.ACTIVE and subscription.end_date:
            subscription.end_date = subscription.end_date + timedelta(days=plan.duration_days or 0)
        else:
            subscription.start_date = date.today()
            subscription.end_date = (
                date.today() + timedelta(days=plan.duration_days)
                if plan.duration_days
                else None
            )
        subscription.status = SubscriptionStatus.ACTIVE
    else:
        payment.status = PaymentStatus.FAILED
        if subscription.status != SubscriptionStatus.ACTIVE:
            subscription.status = SubscriptionStatus.FAILED

    payment.save()
    subscription.save()
    context = {"payment": payment}

    return render(request, "subscriptions/callback.html", context)