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
            resp = HttpResponse('New person was created successfully.', status=201)
            resp["Location"] = "http://127.0.0.1:9000/api/people/{0}".format(p.id)
            resp["x-Created-Id"] = p.id
            return resp


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
    If it is present then blah = <some_status> (string), otherwise blah = None.
    With this we know if we have to filter again or not.
    """
    if request.method == 'GET':
        status = request.GET.get("status")
        queries = Task.objects.filter(owner=p)
        queries = queries if status is None else queries.filter(isDone=True if status == "done" else False)
        return JsonResponse(serialize("json", queries), safe=False)
    elif request.method == 'POST':
        tmp_str = request.body.decode('utf-8')
        json_body = json.loads(tmp_str)
        received_status = "status" in json_body
        is_done = False if not received_status else json_body["status"] == "done"        # New task status set to active by default.
        try:
            t = Task(id=json_body["id"],
                     owner=p,
                     isDone=is_done,
                     details=json_body["details"],
                     dueDate=json_body["dueDate"]
                     )
            t.save()
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)
        else:
            resp = HttpResponse("Task created and assigned successfully",
                                status=201)
            resp["Location"] = "http://127.0.0.1:9000/api/people/{0}/tasks".format(id)
            resp["x-Created-Id"] = "{0}".format(t.id)
            return resp


@require_http_methods(["GET", "PUT"])
@csrf_exempt
def set_task_owner(request, id):
    if request.method == "GET":
        try:
            t = Task.objects.get(id=id)
            p = Person.objects.get(id=t.owner.id)
            return HttpResponse("Owner's id: {0}".format(p.id))
        except Task.DoesNotExist:
            return HttpResponse("Task with id: {0} does not exist.".format(id),
                                status=404
                                )
    elif request.method == "PUT":
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            p = Person.objects.get(id=json_body["id"])
            t = Task.objects.get(id=id)
            t.owner = p
            t.save(update_fields=["owner"])
            return HttpResponse("Task owner updated successfully.", status=204)
        except Person.DoesNotExist:
            return HttpResponse("Person with id: {0} does not exist.".format(json_body["id"]),
                                status=404
                                )
        except Task.DoesNotExist:
            return HttpResponse("Task with id: {0} does not exist.".format(id),
                                status=404
                                )
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)






@require_http_methods(["PUT"])
@csrf_exempt
def set_task_status(request):
    return None

@require_http_methods(["PATCH"])
@csrf_exempt
def patch_task(request):
    return None