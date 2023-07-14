from django.http import HttpResponse
from django.shortcuts import render


def users(request):
    return HttpResponse('Hello, Users')
