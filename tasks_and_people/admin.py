
from django.contrib import admin
from .models import Person, Task

# Monitor the following models
admin.site.register(Person)
admin.site.register(Task)