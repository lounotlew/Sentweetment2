from django.urls import include, path, re_path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	re_path(r'graphs/.*', views.graphs, name = 'graphs')
	]