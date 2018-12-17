"""restful01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from drones import views

app_name = 'drones'
urlpatterns = [
    path('drone-categories/', views.DroneCategoryList.as_view(), name='dronecategory-list'),
    path('drone-categories/<int:pk>/', views.DroneCategoryDetail.as_view(), name='dronecategory-detail'),
    path('drones/', views.DroneList.as_view(), name='drone-list'),
    path('drones/<int:pk>/', views.DroneDetail.as_view(), name='drone-detail'),
    path('pilots/', views.PilotList.as_view(), name='pilot-list'),
    path('pilots/<int:pk>/', views.PilotDetail.as_view(), name='pilot-detail'),
    path('competitions/', views.CompetitionList.as_view(), name='competition-list'),
    path('competitions/<int:pk>/', views.CompetitionDetail.as_view(), name='competition-detail'),
    path('', views.ApiRoot.as_view(),  name='api-root'),
]
