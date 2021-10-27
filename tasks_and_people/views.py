from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def manage_users(request):
    if request.method == 'GET':
        # TODO
    elif request.method == 'SET':
        # TODO


@require_http_methods(["GET", 'DELETE'])
def get_or_delete_person(request):
    return None

@require_http_methods(["GET", "POST"])
def manage_tasks(request):
    if request.method == 'GET':
        # TODO
    elif request.method == 'SET':
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