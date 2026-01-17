from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm
from .models import Profile


# ---------------------------
# Registration View
# ---------------------------
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.save()

            # Create the profile with extra fields
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                imp_code=form.cleaned_data['imp_code'],
                grade=form.cleaned_data['grade'],
                location=form.cleaned_data['location'],
                function_name=form.cleaned_data['function_name'],
                line_manager=form.cleaned_data['line_manager'],
                function_manager=form.cleaned_data['function_manager'],
                functional_head=form.cleaned_data['functional_head'],
            )

            # Show success message and redirect to login
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        else:
            # If form is invalid, show errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ---------------------------
# Login View (basic example)
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('home')  # redirect to dashboard/home
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')


# ---------------------------
# Logout View
# ---------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# ---------------------------
# Forgot Password (UserID based)
# ---------------------------
def forgot_password(request):
    if request.method == "POST":
        userid = request.POST.get("userid")
        try:
            user = User.objects.get(username=userid)  # or use employee code field
            return redirect('reset_password', userid=userid)
        except User.DoesNotExist:
            messages.error(request, "UserID not found.")
    return render(request, "accounts/forgot_password.html")


# ---------------------------
# Reset Password (UserID based)
# ---------------------------
def reset_password(request, userid):
    try:
        user = User.objects.get(username=userid)
    except User.DoesNotExist:
        messages.error(request, "Invalid UserID.")
        return redirect('forgot_password')

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if new_password == confirm_password:
            user.password = make_password(new_password)  # hash before saving
            user.save()
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "accounts/reset_password.html", {"userid": userid})
