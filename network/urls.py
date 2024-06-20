
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("/newpost", views.NewPost, name="newpost"),
    path("user/<str:user>", views.GetUser, name="userprofile"),
    path("follow/<str:username>", views.FollowUser, name="follow"),
    path("follow/", views.FollowingPage, name="followpage"),
    path("like/<int:post_id>", views.LikePost, name="like"),
    path("edit/<int:post_id>", views.EditPost, name="edit"),
]
