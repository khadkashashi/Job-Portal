from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.db.models import Sum
from .forms import JobForm
from .models import Job
from django.views.generic import ListView
from django.db.models import Q
from datetime import date

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
            Q(title__icontains=keyword) | #Q objects allow combining multiple conditions using OR (|) or AND (&).
            Q(company__company_name__icontains=keyword) |
            Q(location__icontains=keyword)
        )
    return render( request, "jobs/job_list.html",{"jobs": jobs})

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job,pk=pk,company__owner=request.user)
    was_expired = job.deadline < date.today()
    if request.method == "POST":
        form = JobForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            if was_expired and job.deadline >= date.today():
                job.is_active = True
                job.save()
                messages.success(request, "Job updated and reactivated - deadline extended.")
            else:
                messages.success(request, "Job updated successfully.")
            return redirect("my-jobs")
              
    else:
        form = JobForm(instance=job)
    return render(request, "jobs/edit_job.html",{"form": form,"job": job})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company__owner=request.user)
    if request.method == "POST":
        job_title = job.title
        job.delete()
        messages.success(request, f"'{job_title}' has been deleted.")
        return redirect("my-jobs")
    return render(request, "jobs/delete_job_confirm.html", {"job": job})

class PublicJobListView(ListView):
    model = Job
    template_name = "jobs/public_job_list.html"
    context_object_name = "jobs" #template ma data jobs naam bata access garna dincha
    paginate_by = 10
    def get_queryset(self): #get_queryset() tells Django-->"Which records should be displayed?"
        queryset = Job.objects.filter(is_active=True, deadline__gte=date.today())  # gte means--> Greater Than or Equal To
        keyword = self.request.GET.get("keyword")
        location = self.request.GET.get("location")
        employment_type = self.request.GET.get("employment_type")
        min_salary = self.request.GET.get("min_salary")

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if employment_type:
            queryset = queryset.filter(employment_type=employment_type)
        if min_salary:
            queryset = queryset.filter(salary_max__gte=min_salary)
        return queryset.order_by("-created_at")
#Why salary_max__gte=min_salary and not salary_min__gte: if someone searches "I want at least 50,000," a job posted as "40,000–60,000" genuinely qualifies (the top of its range clears the bar), but filtering on salary_min__gte=50000 would incorrectly exclude it just because the starting offer happens to be lower. Filtering on salary_max catches every job where 50,000 is actually achievable.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employment_types"] = Job.EmploymentType.choices
        return context


    #get_context_data() is a built-in method used to pass extra data or variables to your HTML template beyond the main query results.