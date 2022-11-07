from django.urls import path
from customer import views


app_name = 'customer'
urlpatterns = [
    path('login/', views.customer_login_signup, name='login'),
    path('login-2/', views.customer_login_signup_2, name='login_2'),
    path('logout/', views.customer_logout, name='logout'),
    path('my-account/', views.my_account, name='my-account'),
]
