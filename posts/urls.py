from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.CreateAndGetPosts.as_view(), name="posts-list-create"),
    path("posts/delete/<int:pk>/", views.DeletePost.as_view(), name="delete-post")
]
