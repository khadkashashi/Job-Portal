from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Company
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
            return redirect("company-profile")

    else:
        form = CompanyForm()

    return render(
        request,
        "companies/create_company.html",
        {"form": form},
    )
@login_required
def company_profile(request):

    if request.user.role != "RECRUITER":
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    company = get_object_or_404(Company,owner=request.user)

    return render( request, "companies/company_profile.html",
        {
            "company": company
        }
    )