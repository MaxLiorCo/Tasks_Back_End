from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from tasks_and_people.models import Person, Task
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse


@require_http_methods(["GET", "POST"])
def manage_users(request):
    if request.method == 'GET':
        all_queries = Person.objects.all()
        data = serialize("json", all_queries)   # JSON representation
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        request_body = request.body()
        p = Person(id=request_body.id, name=request_body.name, email=request_body.email,
                   favoriteProgrammingLanguage=request_body.favoriteProgrammingLanguage)
        p.save()
        return HttpResponse('blyat')


@require_http_methods(["GET", "DELETE"])
def get_or_delete_person(request):
    user_id = request.GET.get('id')             # I HAVE NO CLUE IF THIS WILL WORK
    print(user_id)
    if request.method == 'GET':
        return serialize('json', Person.objects.get(user_id))   # Should return the person that was requested
    elif request.method == 'DELETE':
        Person.objects.get(user_id).delete()


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