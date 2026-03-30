from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_author, name='about_author'),
    path('store/', views.store_info, name='store_info'),
]
