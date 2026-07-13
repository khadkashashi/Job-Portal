from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from jobs.models import Job
from .forms import ApplicationForm
from .models import Application, Applicationstatus

@login_required
def applicant_dashboard(request):
    if request.user.role != "APPLICANT":
        return redirect("dashboard")
    applied_jobs = Application.objects.filter(applicant=request.user).count()
    interview_jobs = Application.objects.filter(applicant=request.user,status=Applicationstatus.SHORTLISTED).count()
    accepted_jobs = Application.objects.filter(applicant=request.user,status=Applicationstatus.HIRED ).count()
    recent_applications = Application.objects.filter(applicant=request.user )[:5]
    recommended_jobs = Job.objects.filter(is_active=True).exclude( applications__applicant=request.user )[:6]
    reviewing_jobs = Application.objects.filter(applicant=request.user,status=Applicationstatus.REVIEWING).count()

    context = {
    "applied_jobs": applied_jobs,
    "reviewing_jobs": reviewing_jobs,
    "interview_jobs": interview_jobs,
    "accepted_jobs": accepted_jobs,
    "recommended_jobs": recommended_jobs,
    "recent_applications": recent_applications,
}
    return render(request,"applications/applicant_dashboard.html",context )

@login_required
def apply_job(request, job_id):
    if request.user.role != "APPLICANT":
        messages.error( request, "Only applicants can apply." )
        return redirect("dashboard")
    job = get_object_or_404(Job,pk=job_id,is_active=True)
    if Application.objects.filter(applicant=request.user,job=job ).exists():
        messages.warning( request, "You have already applied for this job." )
        return redirect( "job-detail", pk=job.pk)

    if request.method == "POST":
        form = ApplicationForm( request.POST,request.FILES )
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()
            messages.success( request, "Application submitted successfully.")
            return redirect("my-applications" )
    else:
        form = ApplicationForm()
    return render( request, "applications/job-apply.html",
        { "form": form, "job": job},
          )


@login_required
def my_applications(request):
    applications = Application.objects.filter( applicant=request.user)
    return render(request,"applications/my_application.html",{"applications": applications})

@login_required
def application_list(request):
    if request.user.role != "RECRUITER":
        return redirect("dashboard")
    applications = Application.objects.filter(job__company__owner=request.user)
    return render(request,"applications/list-application.html", { "applications": applications})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application,pk=pk)
    return render( request,"applications/detail-application.html", { "application": application} )