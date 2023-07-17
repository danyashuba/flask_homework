from django.http import HttpResponse
from django.shortcuts import render

from book.models import Book


def users(request):
    books = Book.objects.values_list()
    return HttpResponse(books)

