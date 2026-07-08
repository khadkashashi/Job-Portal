from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import JobForm


@login_required
def create_job(request):

    if request.user.role != "RECRUITER":
        messages.error(request, "Only recruiters can create jobs.")
        return redirect("dashboard")

    if not hasattr(request.user, "company"):
        messages.warning(request, "Please create your company first.")
        return redirect("create-company")

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.company = request.user.company

            job.save()

            messages.success(request, "Job posted successfully!")

            return redirect("my-jobs")

    else:

        form = JobForm()

    return render(
        request,
        "jobs/create_job.html",
        {
            "form": form,
        },
    )


def my_jobs(request):

    jobs = request.user.company.jobs.all() if hasattr(request.user, "company") else []
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})
