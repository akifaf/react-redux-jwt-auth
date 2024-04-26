from django.contrib import admin
from django.urls import path
from . import views
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes, name='getRoutes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="UserProfileView"),
    path('users/', views.getUsers, name='getUsers'),
    path('register/', views.register, name='register'),
    
    
    path('user-update/<int:pk>/',views.userUpdate,name="user-update"),
    path('user-delete/<int:pk>/',views.userDelete,name="user-delete"),
    path('class-userlist/', ClassUserList.as_view(),name='class-user-list'),


]