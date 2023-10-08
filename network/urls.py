from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.new_post, name="post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following_view, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("check_login_status/", views.check_login_status, name="check_login_status")
]
