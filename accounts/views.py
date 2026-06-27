from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, f"Welcome {user.first_name}!")

            if user.is_superuser:
             return redirect("/admin/")

            return redirect("dashboard")

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")