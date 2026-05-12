from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm


# Kullanıcı kayıt view'i
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# Kullanıcı giriş view'i
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("products:home")

    return render(request, "login.html")


# Kullanıcı çıkış view'i
def user_logout(request):
    logout(request)
    return redirect("products:home")