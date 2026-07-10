from django.shortcuts import render
from jobs.models import Job
from companies.models import Company

def home(request):
    featured_jobs = ( Job.objects.filter(is_active=True).select_related("company").order_by("-created_at")[:8])
    featured_companies = Company.objects.order_by("-created_at")[:6]
    context = {
        "featured_jobs": featured_jobs,
        "featured_companies": featured_companies,
        "total_jobs": Job.objects.filter(is_active=True).count(),
        "total_companies": Company.objects.count(),
    }
    return render(request,"landingpage/home.html", context)
def about(request):
    return render(request, "landingpage/about.html")