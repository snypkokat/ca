from django.contrib import admin
from django.urls import path
from django.views.generic import ListView, DetailView
from appshop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('profile', views.profile),
    path('posts', views.posts),
    path('newpost', views.newpost),
    path('post/<int:id>', views.post),
    path('editpost/<int:id>', views.editpost),
    path('saveeditpost/<int:id>', views.saveeditpost),
    path('deletepost/<int:id>', views.deletepost),
    path('export', views.export),
    path('download', views.download),
    path('registration', views.registration),
    path('login', views.login_user),
    path('logout', views.logout_user),
    
]
