from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import RegisterForm


def auth_view(request):
    form = RegisterForm()

    if request.method == "POST":
        if "register" in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('auth')

        elif "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # later

    return render(request, 'accounts/login_register.html', {'form': form})