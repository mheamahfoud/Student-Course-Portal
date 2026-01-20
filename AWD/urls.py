from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('offerings/', views.offerings, name='offerings'),
    path('logout/', views.logout_view, name='logout'),
    path('api/offerings/', views.api_offerings, name='api_offerings'),
    path('ajax/subscribe/', views.ajax_subscribe, name='ajax_subscribe'),
]