"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.view_published, name='view_published'), # Direct to the published posts view when no url directory is given.
    path('post/<int:primary_key>/', views.view_post, name='view_post'), # Direct to the selected post.
    path('post/new/', views.create_post, name='create_post'), # Create a new Post.
    path('post/edit/<int:primary_key>/', views.edit_post, name='edit_post'), # Direct to the selected post.
    path('post/delete/<int:primary_key>/', views.delete_post, name='delete_post'), # Delete the selected post.
    
    path('posts/all', views.view_all, name='view_all'), # Display all posts.
    path('posts/unpublished', views.view_unpublished, name='view_unpublished'), # Display unpublished posts.
    path('posts/published', views.view_published, name='view_published'), # Display published posts.

    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]