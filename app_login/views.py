from django.shortcuts import render
from django.http import HttpResponse

def minha_view(request):
    return HttpResponse("Olá, mundo! Este é o meu app Django.")

# Create your views here.
