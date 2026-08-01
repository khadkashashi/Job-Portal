from django.shortcuts import render
from django.views.generic import ListView
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