from django.shortcuts import render
from django.http import HttpResponse

from purchase.models import Purchase


def purchase(request):
    purchases = Purchase.objects.values_list()
    return HttpResponse(purchases)
    