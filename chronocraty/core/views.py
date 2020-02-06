from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def healthcheck(request):
    return HttpResponse('Health-check OK')