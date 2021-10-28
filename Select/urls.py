from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login,name='login'),
    path('home', views.index,name='home'),
	path('data', views.data,name='data'),
	path('validate',views.validate,name='validate'),
	path('save/<int:pid>',views.save,name='save'),
	path('addPS', views.addPS, name="addPS"),
	path('updatePS/<str:pk>', views.updatePS, name="updatePS"),
	path('deletePS/<str:pk>', views.deletePS, name="deletePS"),
	path('reset', views.reset, name="reset"),
	path('results', views.results, name="results"),
	path('team_credentials', views.team_credentials, name="team_credentials"),
	path('logout', views.logout, name="logout"),
]