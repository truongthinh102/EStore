from django.urls import path
from cart import views


app_name = 'cart'
urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('remove-cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
