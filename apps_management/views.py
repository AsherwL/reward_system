from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_protect

from .forms import CustomPasswordChangeForm, ProfileUpdateForm
from .models import Task, User

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from apps_management.models import Application


@login_required
def home(request):
    """Renders the home page."""
    return render(request, 'apps_management/home.html')


@login_required
def tasks(request):
    """Renders the tasks page."""
    return render(request, "apps_management/tasks.html")


@login_required
def tasks_view(request):
    """Displays the user's task page."""
    return render(request, "apps_management/tasks.html")


@login_required
@csrf_protect
def profile_view(request):
    """Displays and updates the user's profile."""
    user = request.user

    # Optimization: Retrieve approved tasks and their points in a single query
    total_points = sum(task.application.points for task in Task.objects.filter(user=user, is_approved=True).select_related("application"))

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ProfileUpdateForm(instance=user)

    # Add CSS classes to form fields for better UI styling
    form.fields['username'].widget.attrs.update({
        'class': 'p-2 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
    })
    form.fields['avatar'].widget.attrs.update({
        'class': 'p-2 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
    })

    return render(request, "apps_management/profile.html", {
        "form": form,
        "total_points": total_points,
        "user": user,  # Added `user` for better flexibility in the template
    })


@login_required
def change_password(request):
    """Handles password change functionality."""
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, "Password changed successfully!")
            return redirect("home")  # Redirect to home after success
        else:
            messages.error(request, "Failed to change password. Please check your input.")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "apps_management/change_password.html", {"form": form})


def login_view(request):
    """Handles user login functionality."""
    if request.user.is_authenticated:
        return redirect("home")  # Redirect logged-in users

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "apps_management/login.html", {"error": "Invalid credentials!"})

    return render(request, "apps_management/login.html")


@login_required
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    return redirect("login")


def subscribe_view(request):
    """Allows a user to create an account and log in immediately."""
    if request.user.is_authenticated:
        return redirect("home")  # Redirect if already logged in

    if request.method == "POST":
        username = request.POST.get("username").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check if all fields are filled
        if not username or not password1 or not password2:
            messages.error(request, "All fields are required!")
            return render(request, "apps_management/subscribe.html")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, "apps_management/subscribe.html")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, "apps_management/subscribe.html")

        # Create the user account
        user = User.objects.create_user(username=username, password=password1)

        # Automatically log in the new user
        login(request, user)

        messages.success(request, "Account created successfully! Welcome!")
        return redirect("home")  # Redirect to home page immediately

    return render(request, "apps_management/subscribe.html")



def is_admin(user):
    """Check if the user is an admin or staff member."""
    return user.is_authenticated and user.is_staff  # Vérifie si l'utilisateur est admin/staff

@login_required
@user_passes_test(is_admin)  # Seuls les admins ont accès
def approve_task(request, task_id):
    """Approve a task and assign points to the user."""
    task = get_object_or_404(Task, id=task_id)

    if not task.is_approved:
        task.is_approved = True
        task.save()
        task.user.points += task.application.points  # Assign points to the user
        task.user.save()
        messages.success(request, "✅ Task approved and points assigned.")

    return redirect("/admin/apps_management/task/")  # Redirige vers l'admin Task


@login_required
@user_passes_test(is_admin)  # Seuls les admins ont accès
def reject_task(request, task_id):
    """Reject a task without assigning points."""
    task = get_object_or_404(Task, id=task_id)

    if task.is_approved:
        task.is_approved = False
        task.save()
        messages.success(request, "❌ Task rejected.")

    return redirect("/admin/apps_management/task/")  # Redirige vers l'admin Task
