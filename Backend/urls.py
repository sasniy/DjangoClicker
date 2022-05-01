from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('',views.index,name='index'),
    path('logout/',views.user_logout,name='logout'),
]