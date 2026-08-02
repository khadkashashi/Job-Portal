from django.contrib import messages
from django.contrib.auth import login,logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from companies.models import Company
from jobs.models import Job
from applications.models import Application, Applicationstatus
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from .models import User
from subscriptions.models import Payment, PaymentStatus,CompanyPlan
from django.db.models import Sum



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}!")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            if user.is_superuser or user.role == "ADMIN":
                return redirect("/admin/")
            elif user.role == "RECRUITER":
                return redirect("dashboard")
            elif user.role == "APPLICANT":
                return redirect("applicant-dashboard")
            return redirect("dashboard")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form, "next": next_url})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    company = Company.objects.filter(owner=request.user).first()

    # a company must have picked a plan (even Free) before using the dashboard
    if company and not hasattr(company, "subscription"):
        messages.warning(request, "Please choose a plan to continue.")
        return redirect("choose-plan")

    subscription = getattr(company, "subscription", None) if company else None
    days_remaining = None
    if subscription and subscription.plan.name != "Lifetime" and subscription.end_date:
        days_remaining = (subscription.end_date - timezone.now().date()).days

    jobs = Job.objects.none()
    total_jobs = 0
    active_jobs = 0
    recent_jobs = []
    total_applications = 0
    pending_applications = 0
    reviewing_applications = 0
    shortlisted_applications = 0
    hired_candidates = 0

    if company:
        jobs = Job.objects.filter(company=company)
        total_jobs = jobs.count()
        active_jobs = jobs.filter(is_active=True).count()
        recent_jobs = jobs.order_by("-created_at")[:5]
        applications = Application.objects.filter(job__company=company)
        total_applications = applications.count()
        pending_applications = applications.filter(status=Applicationstatus.PENDING).count()
        reviewing_applications = applications.filter(status=Applicationstatus.REVIEWING).count()
        shortlisted_applications = applications.filter(status=Applicationstatus.SHORTLISTED).count()
        hired_candidates = applications.filter(status=Applicationstatus.HIRED).count()

    context = {
        "company": company,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "recent_jobs": recent_jobs,
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "reviewing_applications": reviewing_applications,
        "shortlisted_applications": shortlisted_applications,
        "hired_candidates": hired_candidates,
        "subscription": subscription,
        "days_remaining": days_remaining,
    }
    return render(request, "accounts/dashboard.html", context)

def admin_dashboard(request):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        messages.error(request, "You don't have access to the admin dashboard.")
        return redirect("login")
    total_applicants = User.objects.filter(role="APPLICANT").count()
    total_recruiters = User.objects.filter(role="RECRUITER").count()
    total_companies = Company.objects.count()
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    total_applications = Application.objects.count()
    total_revenue = Payment.objects.filter(status=PaymentStatus.SUCCESS).aggregate(total=Sum("amount"))["total"] or 0
    recent_companies = Company.objects.order_by("-created_at")[:5]
    recent_users = User.objects.order_by("-created_at")[:5]
    companies = Company.objects.select_related("subscription", "subscription__plan").order_by("company_name")
    paid_plans = CompanyPlan.objects.exclude(name="Free")

    context = {
        "total_applicants": total_applicants,
        "total_recruiters": total_recruiters,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_applications": total_applications,
        "total_revenue": total_revenue,
        "recent_companies": recent_companies,
        "recent_users": recent_users,
        "companies": companies,
        "paid_plans": paid_plans,
    }
    return render(request, "accounts/admin_dashboard.html", context)