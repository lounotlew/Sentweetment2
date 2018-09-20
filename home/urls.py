from django.urls import include, path
from . import views


# URLs for the pages for the main Sentweetment2 home page.
urlpatterns = [
	path('', views.index, name = 'index'),
	path('about', views.about, name = 'about')
	]