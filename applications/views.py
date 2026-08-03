from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from jobs.models import Job
from .forms import ApplicationForm
from .models import AIInterview, Application, Applicationstatus
from .ai import evaluate_interview_answers,generate_interview_questions

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
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin accounts cannot apply to jobs.")
        return redirect("admin-dashboard")
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
            application = form.save(commit=False)#commit=False-->does not save yet.It creates the object in memory only.kina ki applicant ra job field manually set garna baki huncha
            application.applicant = request.user #The logged-in user becomes the applicant.
            application.job = job #The selected job is assigned.
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
    applications = Application.objects.filter( job__company__owner=request.user).select_related( "applicant", "job", "job__company").order_by("-applied_at")
    keyword = request.GET.get("keyword")
    if keyword:
        applications = applications.filter(applicant__username__icontains=keyword)
    status = request.GET.get("status")
    if status:
        applications = applications.filter(status=status)
    applications = applications.order_by("-applied_at")
    context = {
        "applications": applications,
        "keyword": keyword,
        "status": status,
        "pending_applications": Application.objects.filter(job__company__owner=request.user,status=Applicationstatus.PENDING).count(),
        "reviewing_applications": Application.objects.filter( job__company__owner=request.user,status=Applicationstatus.REVIEWING).count(),
        "shortlisted_applications": Application.objects.filter(job__company__owner=request.user,status=Applicationstatus.SHORTLISTED).count(),
        "hired_candidates": Application.objects.filter(job__company__owner=request.user,status=Applicationstatus.HIRED).count(),
        "rejected_candidates": Application.objects.filter(job__company__owner=request.user,status=Applicationstatus.REJECTED).count(),
    }
    return render(request,"applications/list-application.html",context)
        
        
@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, job__company__owner=request.user)
    interview = getattr(application, "aiinterview", None)
    if request.method == "POST":
        new_status = request.POST.get("status")
        valid_statuses = [choice for choice, label in Applicationstatus.choices]
        if new_status in valid_statuses:
            application.status = new_status
            application.save()
            messages.success(request, f"Application marked as {new_status}.")
            notify_statuses = [
                Applicationstatus.REVIEWING,
                Applicationstatus.SHORTLISTED,
                Applicationstatus.HIRED,
                Applicationstatus.REJECTED,
            ]
            if new_status in notify_statuses:
                send_mail(
                    subject=f"Update on your application for {application.job.title}",
                    message=(
                        f"Hi {application.applicant.first_name or application.applicant.username},\n\n"
                        f"Your application for '{application.job.title}' at "
                        f"{application.job.company.company_name} has been updated to: {new_status}.\n\n"
                        f"Log in to your dashboard to see more details.\n\n"
                        f"- {application.job.company.company_name} via JobPortal AI"
                    ),
                    from_email=None, #Django automatically falls back to DEFAULT_FROM_EMAIL from your settings when this is None — one less place to hardcode the sender address.
                    recipient_list=[application.applicant.email],
                    fail_silently=False,#if email sending ever breaks (bad SMTP credentials, network issue, whatever), we don't want that to crash the whole status-update action — the recruiter should still be able to shortlist/reject someone even if the notification email fails behind the scenes. It fails quietly instead of throwing a 500 error at the recruiter.
                )
        else:
            messages.error(request, "Invalid status.")

        return redirect("application-detail", pk=application.pk)

    return render(request,"applications/detail-application.html",{ "application": application, "interview": interview})

@login_required
def start_interview(request, application_id):
    # only the applicant who owns this application can take its interview
    application = get_object_or_404(Application, pk=application_id, applicant=request.user)

    # get_or_create so refreshing this page twice doesn't make two interview rows
    interview, _created = AIInterview.objects.get_or_create(application=application)

    # only ask the AI for questions once - reuse them if the applicant reloads the page
    if not interview.questions:
        interview.questions = generate_interview_questions(application.job)
        interview.save()

    if interview.completed:
        messages.info(request, "You have already completed this interview.")
        return redirect("my-applications")

    return render(
        request,
        "applications/interview.html",
        {"application": application, "interview": interview},
    )


@login_required
def submit_interview(request, application_id):
    application = get_object_or_404(Application, pk=application_id, applicant=request.user)
    interview = get_object_or_404(AIInterview, application=application)
    if request.method == "POST":
        answers = [
            request.POST.get(f"answer_{i}", "").strip()
            for i in range(len(interview.questions))
        ]
        interview.answers = answers
        score, feedback = evaluate_interview_answers(application.job, interview.questions, answers)
        interview.score = score
        interview.feedback = feedback
        interview.completed = True
        interview.save()

        messages.success(request, "Interview submitted! The recruiter will see your AI score.")
        return redirect("my-applications")

    return redirect("start-interview", application_id=application.id)