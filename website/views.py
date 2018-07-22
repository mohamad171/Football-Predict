from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from pymongo import MongoClient

def index(request):
    template = loader.get_template("website/index.html")
    return HttpResponse(template.render())

