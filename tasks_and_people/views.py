from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
import json
from django.contrib.auth.models import User

@require_http_methods(["GET", "POST"])
def manage_users(request):
    if request.method == 'GET':
        resposnse = Person.objects.all()
        #return JsonResponse(resposnse)
        return HttpResponse(resposnse)

    elif request.method == 'POST':
        jsonDict = json.loads(request.POST)
        return HttpResponse("done")


@require_http_methods(["GET"])
def get_person(request):
    # TODO this
    x = 3


