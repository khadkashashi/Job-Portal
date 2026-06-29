from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CompanyForm


@login_required
def create_company(request):
    # Only recruiters can create a company
    if request.user.role != "RECRUITER":
        messages.error(request, "Only recruiters can create a company.")
        return redirect("dashboard")

    # Prevent duplicate company creation
    if hasattr(request.user, "company"):
        messages.info(request, "You already have a company profile.")
        return redirect("dashboard")

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()

            messages.success(request, "Company profile created successfully.")
            return redirect("dashboard")

    else:
        form = CompanyForm()

    return render(
        request,
        "companies/create_company.html",
        {"form": form},
    )