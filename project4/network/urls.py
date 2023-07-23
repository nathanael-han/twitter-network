
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_posts", views.all_posts, name = "all_posts"),
    path("new_posts", views.new_posts, name = "new_posts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user_page/<int:user_id>", views.user_page, name="user_page"),
    path("user_page/<int:user_id>/follow", views.follow, name="follow"),
    path("user_page/<int:user_id>/unfollow", views.unfollow, name="unfollow"),
    path("follow_page/<int:user_id>", views.follow_page, name="follow_page"),
    path("like_post/<int:user_id>/<int:post_id>", views.like_post, name="like_post"),
    path("unlike_post/<int:user_id>/<int:post_id>", views.unlike_post, name="unlike_post"),
    # path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
]
