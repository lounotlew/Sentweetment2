from django.shortcuts import render
from django.http import HttpResponse
from . import tweets
# Create your views here.

def index(request):
	username = request.GET['username']
	context = {'username': username}


	return render(request, "sentiments/analysis.html", context = context)