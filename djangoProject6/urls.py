"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# djangoProject6/urls.py

from django.contrib import admin
from django.urls import path, include
from wakietalkie import views

urlpatterns = [
    path("admin/", admin.site.urls),
    #path('wakietalkie/', include('wakietalkie.urls')),  # wakietalkie 앱의 URL 패턴을 포함
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('<int:pk>/update/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
    # AI 사용자와 관련된 URL 패턴 추가
    path('create/ai_users/', views.ai_user_create, name='ai_user_create'),
    path('create/ai_users/', views.ai_user_list, name='ai_user_list'),
    path('create/ai_users/<int:pk>/', views.ai_user_detail, name='ai_user_detail'),
    path('create/ai_users/<int:pk>/update/', views.ai_user_update, name='ai_user_update'),
    path('create/ai_users/<int:pk>/delete/', views.ai_user_delete, name='ai_user_delete'),
    #serializer
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('ai_users/', views.AIUserListAPIView.as_view(), name='ai_user-list'),
    # CREATE(Create)
    path('users/create/', views.UserCreateAPIView.as_view(), name='user_create'),
    path('ai_users/create/', views.AIUserCreateAPIView.as_view(), name='ai_user_create'),
    # UPDATE(Update)
    path('users/<int:pk>/update/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('ai_users/<int:pk>/update/', views.AIUserUpdateAPIView.as_view(), name='ai_user_update'),
    # DELETE(Delete)
    path('users/<int:pk>/delete/', views.UserDeleteAPIView.as_view(), name='user_delete'),
    path('ai_users/<int:pk>/delete/', views.AIUserDeleteAPIView.as_view(), name='ai_user_delete'),
]

