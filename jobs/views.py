from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.db.models import Sum
from .forms import JobForm
from .models import Job
from django.views.generic import ListView
from django.db.models import Q

FREE_JOB_LIMIT = 10
@login_required
def create_job(request):
    if request.user.role != "RECRUITER":
        messages.error(request, "Only recruiters can create jobs.")
        return redirect("dashboard")
    if not hasattr(request.user, "company"):
        messages.warning(request, "Please create your company first.")
        return redirect("create-company")

    company = request.user.company
    subscription = getattr(company, "subscription", None)
    is_paid_active = subscription and subscription.is_active() and subscription.plan.name != "Free"
    if not is_paid_active and company.jobs.count() >= FREE_JOB_LIMIT:
        messages.error( request, f"Free plan allows {FREE_JOB_LIMIT} job posts. Upgrade your plan to post more.")
        return redirect("choose-plan")

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
    return render( request, "jobs/create_job.html", { "form": form } )

def my_jobs(request):
    jobs = request.user.company.jobs.all() if hasattr(request.user, "company") else []
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404( Job,pk=pk)
    return render( request, "jobs/job_detail.html" ,{"job": job})

def job_list(request):
    jobs = Job.objects.filter( is_active=True).order_by("-created_at")
    keyword = request.GET.get("keyword")
    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(company__company_name__icontains=keyword) |
            Q(location__icontains=keyword)
        )
    return render( request, "jobs/job_list.html",{"jobs": jobs})


class PublicJobListView(ListView):
    model = Job
    template_name = "jobs/public_job_list.html"
    context_object_name = "jobs"
    paginate_by = 10
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        keyword = self.request.GET.get("keyword")
        location = self.request.GET.get("location")
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset.order_by("-created_at")