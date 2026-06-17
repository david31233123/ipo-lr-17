from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='manufacturer')
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')
router.register(r'orders', views.OrderViewSet, basename='order')

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
    
    # Задание 3: URL-маршруты для оформления заказа
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/download/<int:order_id>/', views.download_check, name='download_check'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('api/cart/add/', views.cart_add_api, name='cart_add_api'),
    path('api/me/', views.me_api, name='me_api'),
    path('api/', include(router.urls)),
]
