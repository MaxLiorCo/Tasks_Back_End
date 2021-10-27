from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from tasks_and_people.models import Person, Task

@require_http_methods(["GET", "POST"])
def manage_users(request):
    if request.method == 'GET':
        all_entries = Person.objects.all()
        return all_entries.values()         # JSON representation
    elif request.method == 'SET':
        request_body = request.body()
        p = Person(id=request_body.id, name=request_body.name, email=request_body.email,
                   favoriteProgrammingLanguage=request_body.favoriteProgrammingLanguage)
        p.save()


@require_http_methods(["GET", 'DELETE'])
def get_or_delete_person(request):
    if request.method == 'GET':
    # TODO
    elif request.method == 'DELETE':

@require_http_methods(["GET", "POST"])
def manage_tasks(request):
    if request.method == 'GET':
        # TODO
    elif request.method == 'POST':
        # TODO

@require_http_methods(["PUT"])
def set_task_owner(request):
    return None

@require_http_methods(["PUT"])
def set_task_status(request):
    return None

@require_http_methods(["PATCH"])
def patch_task(request):
    return None