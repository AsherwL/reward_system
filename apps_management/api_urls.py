from django.urls import path
from .api_views import TaskCreateAPI, TaskListAPI

urlpatterns = [
    path("tasks/<int:app_id>/", TaskCreateAPI.as_view(), name="api_tasks_create"),
    # Creates a task associated with a specific application (app_id).

    path("tasks/", TaskListAPI.as_view(), name="api_tasks_list"),
    # Retrieves the list of all tasks for the user.
]
