from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


"""Django view for the main Sentweetment page. Has a single card that takes in a username for
   the user to be analyzed.
   Posts to sentiments.index."""
def index(request):
	return render(request, "home/home.html")


"""Django view for a webpage that contains helpful information about what Sentweetment2 is,
   and how tweets are analyzed.
   Request from home.index."""
def about(request):
	return render(request, "home/about.html")