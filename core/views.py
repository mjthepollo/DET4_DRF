from time import sleep, time

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django_eventstream import send_event


def home(request):
    return render(request, "sse_test.html")


def sse(request):
    start_time = time()
    while True:
        sleep(1)
        print("Hello world!")
        elapsed_time = time() - start_time
        send_event('test', 'message', f'Hello world!({elapsed_time:.2f})')
