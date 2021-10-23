from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def manage_users(request):
    if request.method == 'GET':
        # TODO
    elif request.method == 'SET':
        # TODO


@require_http_methods(["GET"])
def get_person(request):
    # TODO this

