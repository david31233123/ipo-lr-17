from django.urls import path
from . import views

urlpatterns = [
    # Страницы из предыдущего задания
    path('', views.home, name='home'),
    path('about/', views.about_author, name='about_author'),
    path('store/', views.store_info, name='store_info'),
    
    # Задание 1: URL-маршруты для каталога и корзины
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
]
