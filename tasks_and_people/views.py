from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from tasks_and_people.models import Person, Task
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
"""
@require_http_methods : a pre requisite for the request method to enter the view
@csrf_exempt: marks a view as being exempt from the protection ensured by the csrf middleware
"""

"""
checks method type and operates accordingly
GET /people/ : return an array of all Person Objects 
POST /people/ : add a new Person Object to the database
"""
@require_http_methods(["GET", "POST"])
@csrf_exempt
def get_or_create_user(request):
    """
    :return: on GET request - list of people in the database <br> on POST - headers of the location and id of the new person<br>code=201 - Person created successfully<br>code=400 - Required data fields are missing, data makes no sense, or data contains illegal values.
    """
    if request.method == 'GET':
        all_queries = Person.objects.all()
        data = serialize("json", all_queries)  # JSON representation
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        tmp_str = request.body.decode('utf-8')  # Basically converts "bytes" to "string"
        try:
            data_received = json.loads(tmp_str)  # Converts "string" to "json" object
            p = Person(name=data_received["name"],
                       email=data_received["email"],
                       favoriteProgrammingLanguage=data_received["favoriteProgrammingLanguage"],
                       )
            p.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                return HttpResponse('The given "email" field already exists in another Person.',
                                    status=400)
            else:
                return HttpResponse('IntegrityError but unrelated to "email" uniqueness.',
                                    status=400)
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)
        resp = HttpResponse('New person was created successfully.', status=201)
        resp["Location"] = "http://127.0.0.1:9000/api/people/{0}".format(p.id)
        resp["x-Created-Id"] = p.id
        return resp

"""
checks method type and operates accordingly
GET /people/:id : returns a person with the given id (if there is one)
DELETE /people/:id : deletes a person with the given id (if there is one)
PATCH /people/:id : update person fields with the given id (if there is one)
return error if no such person exists
"""
@require_http_methods(["GET", "DELETE", "PATCH"])
@csrf_exempt
def manage_users(request, user_id):
    """
    :param request: http request
    :param user_id: id of a user in the database
    :return: on GET - HttpResponse that contains the details on person with id=user_id<br>on DELETE - if succeeded, HttpResponse with a 'success message'<br>on PATCH - HttpResponse that contains the new details on person with user_id<br>code 200 - Person data provided.<br>code=404 - Requested person is not present<br>code=400 - provided wrong format
    """
    try:
        p = Person.objects.get(id=user_id)
    except Person.DoesNotExist:
        return HttpResponse("Person with id: {0} does not exist.".format(user_id),
                            status=404)
    if request.method == 'GET':
        return JsonResponse(serialize("json", [p]), safe=False,
                            status=200)  # Should return the person that was requested
    elif request.method == 'DELETE':
        p.delete()
        return HttpResponse("Person with id: {0} was deleted successfully.".format(user_id))
    elif request.method == "PATCH":
        try:
            body_json_format = json.loads(request.body.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)
        p.name = body_json_format["name"] if "name" in body_json_format else p.name
        p.email = body_json_format["email"] if "email" in body_json_format else p.email
        p.favoriteProgrammingLanguage = body_json_format[
            "favoriteProgrammingLanguage"] if "favoriteProgrammingLanguage" in body_json_format else p.favoriteProgrammingLanguage
        p.activeTaskCount = body_json_format[
            "activeTaskCount"] if "activeTaskCount" in body_json_format else p.activeTaskCount
        p.save()
        return JsonResponse(serialize('json', [p]), safe=False, status=200)

"""
checks method type and operates accordingly
GET /people/:id/tasks : Returns an array of tasks that the person with id id owns. The optional parameter status allows
                        the caller to filter by task status.
                        When status is not present, return an array of all tasks, regardless os their status.
POST /people/ : Adds the new task, as described by the request body, to the person with the given id.
"""
@require_http_methods(["GET", "POST"])
@csrf_exempt
def person_task_details(request, user_id):
    """
    :param request: http request
    :param user_id: id of a user in the database
    :return: on GET: returns a list of the tasks belong to person with user_id. If optional status field is specified, than all tasks that apply to the status are shown.<br> on POST: adds the new task, as described by the request body, to the person whose id equals id. If the status field is not specified in the request body, the server will default to marking the newly created task as active.<br>code=201: Task created and assigned successfully.<br> code=400: Required data fields are missing, data makes no sense, or data contains illegal values.<br> code=404: Requested person is not present<br>code=400 - provided wrong format
    """
    try:
        p = Person.objects.get(id=user_id)
    except Person.DoesNotExist:
        return HttpResponse("Person with id: {0} does not exist.".format(user_id),
                            status=404
                            )
    """
    http://127.0.0.1:9000/api/people/3/tasks?status=<some_status>.
    With "request.GET.get("status")" we can extract the status (it is a query).
    If it presents then blah = <some_status> (string), otherwise blah = None.
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
        is_done = False if not received_status else json_body[
                                                        "status"] == "done"  # New task status set to active by default.
        if not is_done:
            p.activeTaskCount += 1
            p.save(update_fields=["activeTaskCount"])
        try:
            t = Task(
                     title=json_body["title"],
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
            resp["Location"] = "http://127.0.0.1:9000/api/people/{0}/tasks".format(p.pk)
            resp["x-Created-Id"] = "{0}".format(t.pk)
            return resp

"""
checks method type and operates accordingly
GET /tasks/:id/owner : return owner of the taks with the given id
PUT /tasks/:id/owner : update the owner of the task
"""
@require_http_methods(["GET", "PUT"])
@csrf_exempt
def set_or_get_task_owner(request, task_id):
    """
    :param request: http request
    :param task_id: id of a task in the database
    :return: on GET: id of the owner of the task.<br>on PUT: success message upon successful owner change<br>code=200 - id of the owner of the task.<br>code=404 - requested task is not present.<br>code=204 - task owner updated successfully<br>code=400 - provided wrong format
    """
    try:
        t = Task.objects.get(id=task_id)
        p = Person.objects.get(id=t.owner.id)
    except Task.DoesNotExist:
        return HttpResponse("Task with id: {0} does not exist.".format(task_id),
                            status=404
                            )
    if request.method == "GET":
        return HttpResponse("Owner's id: {0}".format(p.id))
    elif request.method == "PUT":
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            new_owner = Person.objects.get(id=json_body["id"])
            t.owner = new_owner
            new_owner.activeTaskCount = new_owner.activeTaskCount + 1 if not t.isDone else new_owner.activeTaskCount
            p.activeTaskCount = p.activeTaskCount - 1 if not t.isDone else p.activeTaskCount
            p.save(update_fields=["activeTaskCount"])
            new_owner.save(update_fields=["activeTaskCount"])
            t.save(update_fields=["owner"])
            return HttpResponse("Task owner updated successfully.", status=204)
        except Person.DoesNotExist:
            return HttpResponse("Person with id: {0} does not exist.".format(json_body["id"]),
                                status=404
                                )
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)

"""
checks method type and operates accordingly
GET /tasks/:id/status : return task status with the given id
PUT /tasks/:id/status : update task status with the given id
"""
@require_http_methods(["GET", "PUT"])
@csrf_exempt
def set_or_get_task_status(request, task_id):
    """
    :param request: http request
    :param task_id: id of a task in the database
    :return: on GET: provides the current status of task with id=task_id<br> on PUT: update task's status with the given status provided in the body of the http request<br>code=200 - task's current status is provided.<br>code=404 - requested task is not present.<br>code=204 - task's status updated successfully<br>code=400 - provided wrong format
    """
    if request.method == "GET":
        try:
            t = Task.objects.get(id=task_id)
            return HttpResponse("active" if t.isDone is False else "done", status=200)
        except Task.DoesNotExist:
            return HttpResponse("Task with id: {0} does not exist.".format(task_id),
                                status=404
                                )
    elif request.method == "PUT":
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            new_status = json_body["status"]
            if new_status != "active" and new_status != "done":
                return HttpResponse("Value '{0}' is not a legal task status.".format(new_status),
                                    status=400
                                    )
            t = Task.objects.get(id=task_id)
            p = Person.objects.get(id=t.owner.id)
            new_is_done = True if new_status == "done" else False
            # Safe check to make sure that the new value is different than the current one
            if new_is_done != t.isDone:
                if new_is_done:
                    p.activeTaskCount += 1
                else:
                    p.activeTaskCount -= 1
                p.save(update_fields=["activeTaskCount"])
                t.isDone = new_status
                t.save(update_fields=["isDone"])
            return HttpResponse("Status for task id {0} changed to {1} successfully.".format(task_id, new_status))
        except Task.DoesNotExist:
            return HttpResponse("A task with id: {0} does not exist.".format(task_id),
                                status=404
                                )
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)

"""
checks method type and operates accordingly
GET /tasks/:id : returns a task with the given id (if there is one)
DELETE /tasks/:id : deletes a task with the given id (if there is one)
PATCH /tasks/:id : update task fields with the given id (if there is one), fields are optional
return error if no such task exists
"""
@require_http_methods(["GET", "DELETE", "PATCH"])
@csrf_exempt
def manage_tasks(request, task_id):
    """
    :param request: http request
    :param task_id: id of a task in the database
    :return: on GET: provide the details of the task whose id=task_id<br> on DELETE: remove task with id=task_id from the database<br> on PATCH: partial updates of task with id=task_id<br>code=200 - task found and provided/task updated successfully. Data contains updated task/task removed successfully.<br>code=404 - requested task is not present.<br>code=400 - provided wrong format
    """
    try:
        t = Task.objects.get(id=task_id)
        p = Person.objects.get(id=t.owner.id)
    except Task.DoesNotExist:
        return HttpResponse("A task with id: {0} does not exist.".format(task_id),
                            status=404
                            )
    if request.method == "GET":
        print(serialize("json", [t]))
        return JsonResponse(serialize("json", [t]), safe=False, status=200)
    elif request.method == "DELETE":
        t.delete()
        p.activeTaskCount -= 1
        p.save(update_fields=["activeTaskCount"])
        return HttpResponse("Task removed successfully.", status=200)
    elif request.method == "PATCH":
        try:
            body_json_format = json.loads(request.body.decode("utf-8"))
            t.title = body_json_format["title"] if "title" in body_json_format else t.title
            t.details = body_json_format["details"] if "details" in body_json_format else t.details
            t.dueDate = body_json_format["dueDate"] if "dueDate" in body_json_format else t.dueDate
            # Handling owner change
            if "ownerId" in body_json_format:
                new_owner = Person.objects.get(id=body_json_format["ownerId"])
                new_owner.activeTaskCount = new_owner.activeTaskCount + 1 if not t.isDone else new_owner.activeTaskCount
                p.activeTaskCount = new_owner.activeTaskCount - 1 if not t.isDone else p.activeTaskCount
                new_owner.save(update_fields=["activeTaskCount"])
                p.save(update_fields=["activeTaskCount"])
                t.owner = new_owner
            # Handling task status
            if "status" in body_json_format:
                new_is_done = True if body_json_format["status"] == "done" else False
                # Safe check to make sure that the new value is different than the current one
                if new_is_done != t.isDone:
                    if new_is_done:
                        t.owner.activeTaskCount += 1
                    else:
                        t.owner.activeTaskCount -= 1
                    t.owner.save(update_fields=["activeTaskCount"])
                    t.isDone = new_is_done
            # Pushing the updated task
            t.save()
            return JsonResponse(serialize('json', [t]), safe=False, status=200)
        except Person.DoesNotExist:
            return HttpResponse("Person with id: {0} does not exist.".format(body_json_format["id"]),
                                status=404
                                )
        except json.decoder.JSONDecodeError:
            return HttpResponse('Required data fields are missing, data makes no sense, or data contains illegal '
                                'values.',
                                status=400)
