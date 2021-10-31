"""Tasks_Back_End URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from tasks_and_people import views

urlpatterns = [
    path('people/', views.get_or_create_user),
    path('people/<int:user_id>', views.manage_users),
    path('people/<int:user_id>/tasks', views.person_task_details),
    path('tasks/<int:task_id>/owner', views.set_or_get_task_owner),
    path('tasks/<int:task_id>/status', views.set_or_get_task_status),
    path('tasks/<int:task_id>', views.manage_tasks),
]
