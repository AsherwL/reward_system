from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
from .models import User, Task, Application

# Unregister the Group model (not needed here)
admin.site.unregister(Group)


### USER ADMIN ###
class TaskInline(admin.TabularInline):
    """Display tasks associated with a user directly in the admin user profile."""
    model = Task
    extra = 0
    readonly_fields = ("application", "is_approved", "created_at", "task_screenshot_preview")
    can_delete = False

    def task_screenshot_preview(self, obj):
        """Show an image preview that is clickable to view full size."""
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="100" height="100" style="border-radius:5px;"/></a>',
                obj.screenshot.url, obj.screenshot.url)
        return "No Screenshot Uploaded"

    task_screenshot_preview.short_description = "Screenshot Preview"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the User model."""
    list_display = ("username", "email", "total_approved_points", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    readonly_fields = ("total_approved_points",)
    inlines = [TaskInline]

    def total_approved_points(self, obj):
        """Show total approved points for the user."""
        total_points = sum(task.application.points for task in Task.objects.filter(user=obj, is_approved=True))
        return total_points

    total_approved_points.short_description = "Total Approved Points"


### APPLICATION ADMIN ###
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin configuration for the Application model."""
    list_display = ("name", "category", "points")
    search_fields = ("name", "category")


### TASK ADMIN ###
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for the Task model."""
    list_display = (
    "user_link", "application_link", "task_screenshot_preview", "task_status", "approve_button", "reject_button",
    "created_at")
    search_fields = ("user__username", "application__name")
    list_filter = ("is_approved",)
    actions = ["approve_tasks", "reject_tasks"]
    readonly_fields = ("task_screenshot_preview",)

    def user_link(self, obj):
        """Clickable link to the user profile."""
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>',
                           User._meta.app_label,
                           User._meta.model_name,
                           obj.user.id,
                           obj.user.username)

    user_link.short_description = "User"

    def application_link(self, obj):
        """Clickable link to the related application."""
        return format_html('<a href="/admin/{}/{}/{}/change/">{}</a>',
                           Application._meta.app_label,
                           Application._meta.model_name,
                           obj.application.id,
                           obj.application.name)

    application_link.short_description = "Application"

    def task_status(self, obj):
        """Show the current status of the task (Pending, Approved, Rejected)."""
        if obj.is_approved:
            return format_html('<span style="color: green;">✔ Approved</span>')
        elif obj.is_approved is False:
            return format_html('<span style="color: red;">❌ Rejected</span>')
        return format_html('<span style="color: orange;">⏳ Pending</span>')

    task_status.short_description = "Status"

    def task_screenshot_preview(self, obj):
        """Show a clickable screenshot preview."""
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="100" height="100" style="border-radius:5px;"/></a>',
                obj.screenshot.url, obj.screenshot.url)
        return "No Screenshot Uploaded"

    task_screenshot_preview.short_description = "Screenshot"

    def approve_button(self, obj):
        """Show an approve button always."""
        approve_url = reverse("approve_task", args=[obj.id])
        return format_html(
            '<a class="button" style="background-color:green; color:white; padding:5px 10px; border-radius:5px;" href="{}">✅ Approve</a>',
            approve_url)

    approve_button.short_description = "Approve"

    def reject_button(self, obj):
        """Show a reject button always."""
        reject_url = reverse("reject_task", args=[obj.id])
        return format_html(
            '<a class="button" style="background-color:red; color:white; padding:5px 10px; border-radius:5px;" href="{}">❌ Reject</a>',
            reject_url)

    reject_button.short_description = "Reject"

    def approve_tasks(self, request, queryset):
        """Approve tasks and assign points."""
        for task in queryset:
            if not task.is_approved:
                task.is_approved = True
                task.save()
                task.user.points += task.application.points
                task.user.save()
        self.message_user(request, "✅ Selected tasks have been approved and points assigned.")

    def reject_tasks(self, request, queryset):
        """Reject tasks."""
        queryset.update(is_approved=False)
        self.message_user(request, "❌ Selected tasks have been rejected.")

    approve_tasks.short_description = "✅ Approve selected tasks"
    reject_tasks.short_description = "❌ Reject selected tasks"
