from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from tasks_and_people.models import Person, Task

@require_http_methods(["GET", "POST"])
def manage_users(request):
    if request.method == 'GET':
        all_entries = Person.objects.all()
        return all_entries.values()         # JSON representation
    elif request.method == 'POST':
        request_body = request.body()
        p = Person(id=request_body.id, name=request_body.name, email=request_body.email,
                   favoriteProgrammingLanguage=request_body.favoriteProgrammingLanguage)
        p.save()


@require_http_methods(["GET", 'DELETE'])
def get_or_delete_person(request):
    user_id = request.GET.get('id')  # I HAVE NO CLUE IF THIS WILL WORK
    if request.method == 'GET':
        return Person.objects.get(id=user_id)   # Should return the person that was requested
    elif request.method == 'DELETE':
        Person.objects.get(id=user_id).delete()


@require_http_methods(["GET", "POST"])
def manage_tasks(request):
    if request.method == 'GET':
        # TODO
        None
    elif request.method == 'POST':
        # TODO
        None

@require_http_methods(["PUT"])
def set_task_owner(request):
    return None

@require_http_methods(["PUT"])
def set_task_status(request):
    return None

@require_http_methods(["PATCH"])
def patch_task(request):
    return None