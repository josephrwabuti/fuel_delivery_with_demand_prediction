from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import Profile
from django.contrib.auth.decorators import login_required


@login_required
def customer_dashboard(request):
    return render(request, 'dashboard/customerdashboard/dashboard.html')

@login_required
def driver_dashboard(request):
    return render(request, 'dashboard/driverdashboard/dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admindashboard/dashboard.html')



def auth_view(request):
    print("POST RECIEVED")
    print(request.POST)
    
    form = RegisterForm()

    if request.method == "POST":
        if "register" in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                
                print("FORM VALID")
                
                user = form.save(commit=False)
                
                user.username = form.cleaned_data['email']
                
                user.save()
                
                
                print("USER SAVED:", user.username)
                
                
                Profile.objects.create(user=user, role='customer')
                
                Profile.objects.create(user=user, role='driver')
                
                print("USER SAVED:", user.username)
                
                return redirect('auth')
            
            else:
                print("FORM ERRORS:", form.errors)

        elif "login" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")
            
            print("EMAIL:", email)

            user = authenticate(request, username=email, password=password)
            print("AUTH RESULT:", user)

            if user is not None:
                login(request, user)
                
                profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'customer'})
                
                print("ROLE:", profile.role)
                
                
                
                
                if profile.role == 'customer':
                    return redirect('customer_dashboard')
                
                elif profile.role == 'driver':
                    return redirect('driver_dashboard')
                
                elif profile.role == 'admin':
                    return redirect('admin_dashboard')
            
            else:
                print("LOGIN FAILED")
                
    return render(request, 'accounts/login_register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('auth')

