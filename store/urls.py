from django.urls import path
from store import views


app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('subcategory/<int:pk>/', views.subcategory, name='subcategory'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>/', views.product, name='product'),
    path('user/', views.demo_user, name='user'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('product-service/', views.product_service, name='product_service'),
    path('product-service/<int:pk>/', views.product_service_number, name='product_service_number'),

]
