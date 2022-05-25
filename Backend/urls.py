from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

boosts = views.BoostViewSet.as_view({
    'get': 'list', # Получить список всех бустов
    'post': 'create', # Создать буст
})

urlpatterns = [
    path('call_click/', views.call_click),
    path('', views.index, name='index'),
    path('boosts/', boosts, name='boosts'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('login/',views.Login.as_view(),name='login'),
    path('register',views.Register.as_view(),name='register'),
    path('buy_boost/<pk>',views.call_boost,name='buy_boost'),
]