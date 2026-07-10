from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def application_list(request):
    return render(request, "applications/list-appication.html")