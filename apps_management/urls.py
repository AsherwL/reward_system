from django.urls import path, include
from .api_views import ApplicationListCreateAPI, ApplicationDetailAPI, TaskCreateAPI, TaskListAPI
from .views import home, profile_view, login_view, logout_view, tasks_view, change_password, subscribe_view, \
    approve_task, reject_task

urlpatterns = [
    # Main pages (still using Django Templates)
    path('', home, name='home'),
    path('profile/', profile_view, name='profile'),
    path("profile/change-password/", change_password, name="change_password"),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path("subscribe/", subscribe_view, name="subscribe"),
    path("tasks/", tasks_view, name="tasks"),

    # API URLs
    path("api/", include("apps_management.api_urls")),  # Includes API URLs from apps_management

    # API for applications
    path("apps/", ApplicationListCreateAPI.as_view(), name="api_apps"),  # GET & POST (Admin)
    path("apps/<int:app_id>/", ApplicationDetailAPI.as_view(), name="api_app_detail"),  # POST & DELETE (Admin)

    # API for tasks (replaces `upload_task`)
    path("tasks/<int:app_id>/", TaskCreateAPI.as_view(), name="api_tasks_create"),  # Upload task
    path("tasks/", TaskListAPI.as_view(), name="api_tasks_list"),  # View user's tasks



    path("tasks/approve/<int:task_id>/", approve_task, name="approve_task"),
    path("tasks/reject/<int:task_id>/", reject_task, name="reject_task"),
]

