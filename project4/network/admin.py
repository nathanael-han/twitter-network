from django.contrib import admin

# Register your models here.
from .models import NewPost, User

admin.site.register(User)
admin.site.register(NewPost)
