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
from toys import views

app_name = 'toys'
urlpatterns = [
    path('', views.toy_list, name='home'),
    path('<int:pk>/', views.toy_detail, name='detail'),
    path('cbv/', views.ToyListCBV.as_view(), name='cbv_home'),
    path('cbv/<int:pk>/', views.ToyDetailCBV.as_view(), name='cbv_detail'),
    path('cbv_mixin/', views.ToyListMixin.as_view(), name='cbv_mixin_home'),
    path('cbv_mixin/<int:pk>/', views.ToyDetailMixin.as_view(), name='cbv_mixin_detail'),
    path('cbv_generic/', views.ToyGenericCBVList.as_view(), name='cbv_generic_home'),
    path('cbv_generic/<int:pk>/', views.ToyGenericCBVDetail.as_view(), name='cbv_generic_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
