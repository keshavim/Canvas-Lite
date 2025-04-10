from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


def TheApp(request):
    template = loader.get_template("theapp.html")
    return HttpResponse(template.render())


def RemoveThisLater(request):
    template = loader.get_template("tempfile.html")
    return HttpResponse(template.render())