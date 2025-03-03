from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404

from apps_management.models import Application, Task


class ApplicationListCreateAPI(View):
    """
    API to list and create applications.

    - GET: Returns applications that the user has not yet subscribed to.
    - POST: Allows admin to add a new application.
    """

    @method_decorator(login_required)
    def get(self, request):
        # Get applications that the user has already submitted a task for
        subscribed_apps = Task.objects.filter(user=request.user).values_list("application_id", flat=True)

        # Filter out applications that the user has not subscribed to
        apps = Application.objects.exclude(id__in=subscribed_apps)

        return render(request, "partials/apps_list.html", {"apps": apps})

    @method_decorator(login_required)
    def post(self, request):
        # Ensure only admins can add applications
        if not request.user.is_staff:
            return HttpResponseForbidden("❌ You are not authorized to add applications.")

        # Retrieve application details from the request
        name = request.POST.get("name")
        link_app = request.POST.get("link_app")
        download_link = request.POST.get("download_link")
        points = request.POST.get("points")
        category = request.POST.get("category")
        default_logo = request.POST.get("default_logo", None)
        custom_logo = request.FILES.get("custom_logo", None)

        # Validate that required fields are provided
        if name and link_app and download_link and points and category:
            Application.objects.create(
                name=name,
                link_app=link_app,
                download_link=download_link,
                points=points,
                category=category,
                default_logo=default_logo,
                custom_logo=custom_logo
            )
            return JsonResponse({"message": "✅ Application created successfully."})
        return JsonResponse({"error": "❌ Missing fields."}, status=400)


class ApplicationDetailAPI(View):
    """
    API to update or delete an application (Admin only).
    """

    @method_decorator(login_required)
    def post(self, request, app_id):
        # Ensure only admins can update applications
        if not request.user.is_staff:
            return HttpResponseForbidden("❌ You are not authorized to update applications.")

        # Retrieve the application
        app = get_object_or_404(Application, id=app_id)

        # Update application details
        app.name = request.POST.get("name", app.name)
        app.link_app = request.POST.get("link_app", app.link_app)
        app.download_link = request.POST.get("download_link", app.download_link)
        app.points = request.POST.get("points", app.points)
        app.category = request.POST.get("category", app.category)

        # Handle logos
        default_logo = request.POST.get("default_logo", app.default_logo)
        custom_logo = request.FILES.get("custom_logo", app.custom_logo)

        app.default_logo = default_logo
        if custom_logo:
            app.custom_logo = custom_logo

        app.save()
        return JsonResponse({"message": "✅ Application updated successfully."})

    @method_decorator(login_required)
    def delete(self, request, app_id):
        # Ensure only admins can delete applications
        if not request.user.is_staff:
            return HttpResponseForbidden("❌ You are not authorized to delete applications.")

        # Retrieve and delete the application
        app = get_object_or_404(Application, id=app_id)
        app.delete()
        return JsonResponse({"message": "✅ Application deleted successfully."})


class TaskCreateAPI(View):
    """
    API to submit a task with a screenshot as proof.
    """

    @method_decorator(login_required)
    def get(self, request, app_id):
        """Returns the upload form for a task submission."""
        print(f"🔍 HTMX request received for app {app_id}")
        app = get_object_or_404(Application, id=app_id)
        return render(request, "partials/task_upload.html", {"app": app})

    @method_decorator(login_required)
    def post(self, request, app_id):
        """Allows a user to submit a screenshot as proof of app download."""
        app = get_object_or_404(Application, id=app_id)

        # Ensure a screenshot is uploaded
        if 'screenshot' not in request.FILES:
            return JsonResponse({"error": "❌ Screenshot is required."}, status=400)

        screenshot = request.FILES['screenshot']

        # Save the task
        task = Task.objects.create(
            user=request.user,
            application=app,
            screenshot=screenshot,
            is_approved=False  # Needs admin approval
        )

        # ✅ Add HTMX header for redirection after upload
        response = JsonResponse({"message": "✅ Task submitted successfully. Waiting for approval!"})
        response["HX-Redirect"] = "/tasks/"  # Redirect after success
        return response


class TaskListAPI(View):
    """
    API to retrieve all tasks submitted by the logged-in user with filtering options.
    """

    @method_decorator(login_required)
    def get(self, request):
        """Fetches tasks based on approval status."""

        # Retrieve the filter parameter
        filter_status = request.GET.get("status", "all")

        # Apply filtering
        if filter_status == "approved":
            tasks = Task.objects.filter(user=request.user, is_approved=True)
        elif filter_status == "rejected":
            tasks = Task.objects.filter(user=request.user, is_approved=False, screenshot__isnull=True)  # Rejected = No screenshot
        elif filter_status == "pending":
            tasks = Task.objects.filter(user=request.user, is_approved=False, screenshot__isnull=False)  # Pending approval
        else:
            tasks = Task.objects.filter(user=request.user)  # All tasks

        # Check if it's an HTMX request and return only the task list
        if "HX-Request" in request.headers:
            return render(request, "partials/tasks_list.html", {"tasks": tasks})

        return render(request, "partials/tasks.html", {"tasks": tasks})
