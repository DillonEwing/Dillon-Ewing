# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/new/", views.PostCreateView.as_view(), name="blog_post_create"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("user/<str:username>/", views.blog_user_posts, name="blog_user_posts"),
    path("category/<category>/", views.blog_category, name="blog_category"),
]