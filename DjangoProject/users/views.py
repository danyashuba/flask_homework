from django.http import HttpResponse
from django.shortcuts import render

from users.models import User


def users(request):
    user = User.objects.values_list()
    return HttpResponse(user)
