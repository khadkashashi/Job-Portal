from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import JobForm


@login_required
def create_job(request):

    # Only recruiters can post jobs
    if request.user.role != "RECRUITER":
        messages.error(request, "Only recruiters can create jobs.")
        return redirect("dashboard")

    # Recruiter must have a company
    if not hasattr(request.user, "company"):
        messages.warning(request, "Please create your company profile first.")
        return redirect("create-company")

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.company = request.user.company

            job.save()

            messages.success(request, "Job posted successfully.")

            return redirect("my-jobs")

    else:

        form = JobForm()

    return render(
        request,
        "jobs/create_job.html",
        {
            "form": form
        },
    )
@login_required
def my_jobs(request):

    if request.user.role != "RECRUITER":
        return redirect("dashboard")

    jobs = request.user.company.jobs.all().order_by("-created_at")

    return render(
        request,
        "jobs/my_jobs.html",
        {
            "jobs": jobs
        },
    )