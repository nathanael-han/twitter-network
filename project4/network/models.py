from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="followers")
    

class NewPost(models.Model):
    """This model creates fields required for a new post"""
    post = models.TextField(max_length=128)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="posts_liked")


    #: source for ordering data:
    #: https://stackoverflow.com/questions/7945124/how-do-i-show-recent-posts-first-in-django-blog
    class Meta:
        ordering = ['-timestamp',]

