from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('user_detail/', views.user_detail_view, name='user_detail'),
    path('logout/', views.logout_view, name='logout'),
]