from django.urls import path

from .views import posts, post

urlpatterns = [
    # all posts
    path('posts/', posts, name='posts'),
    # all post from a specific user
    path('posts/<str:username>/', posts, name='posts'),
    path('post/<str:pk>/', post, name='post'),
]