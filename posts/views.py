from django.shortcuts import HttpResponse
from datetime import date

def main(request):
    return HttpResponse('Django project')


def hello(request):
    return HttpResponse('Hello! Its my project')


def now_date(request):
    return HttpResponse(f'Today is {date.today()}')


def gb(request):
    return  HttpResponse('Goodby user!')