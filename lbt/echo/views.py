#!coding: utf-8
from django.http import StreamingHttpResponse

def echo(request):
    return StreamingHttpResponse('echo')
