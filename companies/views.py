from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Company
from .forms import CompanyForm
from subscriptions.models import CompanyPlan, CompanySubscription, SubscriptionStatus
from datetime import date


@login_required
def create_company(request):
    if request.user.role != "RECRUITER":
        messages.error(request, "Only recruiters can create a company.")
        return redirect("dashboard")
    if hasattr(request.user, "company"):
        messages.info(request, "You already have a company profile.")
        return redirect("dashboard")
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            wants_paid_plan = request.POST.get("wants_paid_plan") == "yes"

            if wants_paid_plan:
                messages.success(request, "Company created! Now choose your plan.")
                return redirect("choose-plan")

            free_plan = CompanyPlan.objects.get(name="Free")
            CompanySubscription.objects.create(
                company=company,
                plan=free_plan,
                status=SubscriptionStatus.ACTIVE,
                start_date=date.today(),
                end_date=None,
            )
            messages.success(request, "Company created on the Free plan.")
            return redirect("dashboard")
    else:
        form = CompanyForm()
    return render(request,"companies/create_company.html",{"form": form})

@login_required
def company_profile(request):
    if request.user.role != "RECRUITER":
        messages.error(request, "Access denied.")
        return redirect("dashboard")
    company = get_object_or_404(Company, owner=request.user)
    return render(request, "companies/company_profile.html", {"company": company})


@login_required
def company_detail(request, pk):
    company = get_object_or_404(
        Company,
        pk=pk,
    )
    return render( request,"companies/company_detail.html",{"company": company})


@login_required
def edit_company(request, pk):

    company = get_object_or_404(
        Company,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":

        form = CompanyForm(
            request.POST,
            request.FILES,
            instance=company,
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Company updated successfully.")

            return redirect(
                "company-detail",
                pk=company.pk,
            )

    else:

        form = CompanyForm(instance=company)

    return render(
        request,
        "companies/edit_company.html",
        {
            "form": form,
            "company": company,
        },
    )
def company_list(request):
    companies = Company.objects.all().order_by("-created_at")
    return render( request,"companies/company_list.html",
        {
            "companies": companies,
        },
    )