from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import Job

from .forms import ApplicationForm
from .models import Application


@login_required
def apply_job(request, job_id):

    if request.user.role != "JOB_SEEKER":
        messages.error(
            request,
            "Only applicants can apply.",
        )
        return redirect("dashboard")

    job = get_object_or_404(
        Job,
        pk=job_id,
        is_active=True,
    )

    if Application.objects.filter(
        applicant=request.user,
        job=job,
    ).exists():

        messages.warning(
            request,
            "You have already applied for this job.",
        )

        return redirect(
            "job-detail",
            job.pk,
        )

    if request.method == "POST":

        form = ApplicationForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            application = form.save(
                commit=False,
            )

            application.applicant = request.user

            application.job = job

            application.save()

            messages.success(
                request,
                "Application submitted successfully.",
            )

            return redirect(
                "my-applications",
            )

    else:

        form = ApplicationForm()

    return render(
        request,
        "applications/apply_job.html",
        {
            "form": form,
            "job": job,
        },
    )


@login_required
def my_applications(request):

    applications = Application.objects.filter(applicant=request.user),

    return render(request, "applications/my_applications.html",
        {
            "applications": applications,
        },
    )


@login_required
def application_list(request):

    if request.user.role != "RECRUITER":

        return redirect("dashboard")

    applications = Application.objects.filter(
        job__company__owner=request.user,
    )

    return render(
        request,
        "applications/list-application.html",
        {
            "applications": applications,
        },
    )


@login_required
def application_detail(request, pk):

    application = get_object_or_404(
        Application,
        pk=pk,
    )

    return render(
        request,
        "applications/detail-application.html",
        {
            "application": application,
        },
    )