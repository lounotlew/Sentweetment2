from django.urls import include, path, re_path
from . import views

# URL patterns for pages related to the sentiment app.
urlpatterns = [
	path('', views.index, name = 'index'),
	re_path(r'graphs/.*', views.graphs, name = 'graphs'),
	re_path(r'all-tweets/.*', views.all_tweets, name = 'all_tweets'),
	re_path(r'searched-tweets/.*', views.searched_tweets, name = 'searched_tweets')
	]