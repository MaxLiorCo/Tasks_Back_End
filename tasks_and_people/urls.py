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
from django.contrib import admin
from django.urls import path
from tasks_and_people import views

urlpatterns = [
    path('people/', views.manage_users),                        # Either 'GET' or 'POST'
    path('people/<int:id>', views.get_or_delete_person),        # 'GET', 'DELETE'
    path('people/<int:id>/tasks', views.manage_tasks),
    path('tasks/<int:id>/owner', views.set_task_owner),
    path('tasks/<int:id>/isDone', views.set_task_status),
    path('tasks/<int:id>', views.patch_task),
]
