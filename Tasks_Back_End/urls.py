from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

"""
Main URL patterns of the project

admin:
Allows birds eye view on the entire project, managing the different database tables, requires admin registration via 
'python manage.py createsuperuser' command in root directory.

api:
The main app we deploy in this project, through it we operate on Person and Taks databases.
various functionalities specified in the main html file.
"""
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/', include('tasks_and_people.urls')),
]