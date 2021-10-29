from django.db import IntegrityError
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from tasks_and_people.models import Person, Task
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@require_http_methods(["GET", "POST"])
@csrf_exempt
def manage_users(request):
    if request.method == 'GET':
        all_queries = Person.objects.all()
        data = serialize("json", all_queries)       # JSON representation
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        tmp_str = request.body.decode('utf-8')      # Basically converts "bytes" to "string"
        # TODO
        """
        There is a problem here - the uniqueness of the 'id' isn't preserved for some reason.
        When adding a new person with id x and there's already a person with the same id in the db,
        no errors are thrown, and the old person fields are replaced with the new values of the new one.
        """
        try:
            data_received = json.loads(tmp_str)     # Converts "string" to "json" object
            p = Person(id=data_received["id"],
                       name=data_received["name"],
                       email=data_received["emails"],
                       favoriteProgrammingLanguage=data_received["favoriteProgrammingLanguage"],
                       activeTaskCount=data_received["activeTaskCount"]
                       )
            p.save()
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.', 
                                status=400)
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                return HttpResponse('A person with this id already exists!', status=400)
        else:
            return HttpResponse('New person was created successfully.', status=201)


@require_http_methods(["GET", "DELETE"])
@csrf_exempt
def get_or_delete_person(request, id):
    try:
        p = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return HttpResponse("Person with id: {0} does not exist.".format(id),
                            status=404)
    if request.method == 'GET':
        return JsonResponse(serialize("json", [p]), safe=False, status=200)   # Should return the person that was requested
    elif request.method == 'DELETE':
        p.delete()
        return HttpResponse("Person with id: {0} was deleted successfully.".format(id))


@require_http_methods(["GET", "POST"])
@csrf_exempt
def manage_tasks(request, id):
    try:
        p = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return HttpResponse("Person with id: {0} does not exist.".format(id),
                            status=404
                            )
    """
    http://127.0.0.1:9000/api/people/3/tasks?status=<some_status>.
    With "request.GET.get("status")" we can extract the status (it is a query).
    If it is present then blah = <some_status> (probably a string), otherwise blah = None.
    With this we know if we have to filter again or not.
    """
    blah = request.GET.get("status")
    print(blah)
    tmp_str = request.body.decode('utf-8')
    received_status = False
    status = False
    if "status" in tmp_str:
        body = json.loads(tmp_str)
        status = False if body["status"] == "active" else True
        received_status = True
    if request.method == 'GET':
        queries = Task.objects.filter(owner=p)
        queries = queries if not received_status else queries.filter(isDone=status)
        return JsonResponse(serialize("json", queries), safe=False)
    elif request.method == 'POST':
        # TODO
        None

@require_http_methods(["PUT"])
@csrf_exempt
def set_task_owner(request):
    return None

@require_http_methods(["PUT"])
@csrf_exempt
def set_task_status(request):
    return None

@require_http_methods(["PATCH"])
@csrf_exempt
def patch_task(request):
    return None