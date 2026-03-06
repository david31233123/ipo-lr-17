from django.urls import path
from .views import home, author, shop

urlpatterns = [
    path('', home, name='home'),
    path('author/', author, name='author'),
    path('shop/', shop, name='shop')
]
