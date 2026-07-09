from django.contrib import messages
from django.contrib.auth import login,logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from companies.models import Company
from jobs.models import Job


@login_required
def dashboard(request):

    company = Company.objects.filter(owner=request.user).first()

    total_jobs = 0
    active_jobs = 0

    if company:
        total_jobs = Job.objects.filter(company=company).count()
        active_jobs = Job.objects.filter(
            company=company,
            is_active=True
        ).count()

    context = {
        "company": company,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )

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

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, f"Welcome {user.first_name}!")

            if user.is_superuser:
             return redirect("/admin/")

            return redirect("dashboard")

    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):

    company = Company.objects.filter(owner=request.user).first()

    jobs = Job.objects.none()
    total_jobs = 0
    active_jobs = 0
    recent_jobs = []

    if company:
        jobs = Job.objects.filter(company=company)

        total_jobs = jobs.count()

        active_jobs = jobs.filter(is_active=True).count()

        recent_jobs = jobs.order_by("-created_at")[:5]

    context = {
        "company": company,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "recent_jobs": recent_jobs,

        # We'll replace this later with real data
        "total_applications": 0,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )