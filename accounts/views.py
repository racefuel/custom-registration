from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


# Create your views here.
def home(request):
    return render(request, "accounts/home.html")


def signup(request):
    if request.method == "POST":
        if request.POST["password0"] == request.POST["password1"]:
            try:
                user = User.objects.get(email=request.POST["email"])
                return render(
                    request,
                    "accounts/signup.html",
                    {"error": "Email already registered!"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST["email"],
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    password=request.POST["password0"],
                )
                auth.login(request, user)
                return redirect("home")
        else:
            return render(
                request, "accounts/signup.html", {"error": "Passwords do not match!"}
            )
    else:
        return render(request, "accounts/signup.html")


def login(request):
    if request.method == "POST":
        user = auth.authenticate(
            email=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            return redirect("profile")
        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "Email or Password is incorrect!"},
            )
    else:
        return render(request, "accounts/login.html")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return render(request, "accounts/login.html")


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile successfully updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "accounts/profile.html", context)

