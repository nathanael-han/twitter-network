import re
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.core.paginator import Paginator


from .models import User, NewPost


class CreateNewPost(ModelForm):
    class Meta:
        model = NewPost
        fields = ["post"]


def index(request):
    """This view renders the index page"""
    return render(request, "network/index.html")


def all_posts(request):
    """This view displays all posts"""
    #  source: https://docs.djangoproject.com/en/4.0/topics/pagination/
    posts = NewPost.objects.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    postform = CreateNewPost()
    return render(request, "network/all_posts.html", {
        "page_obj": page_obj,
        "form": postform,
    })

def follow_page(request, user_id):
    """This view renders the following page"""

    current_following = User.objects.get(id=user_id).following.all() # gets the users followed
    posts = NewPost.objects.filter(author__in=current_following) # gets the posts made by users followed
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/follow_page.html", {
        "page_obj": page_obj,
    })

def new_posts(request):
    """This view renders the new post form and submits a post"""
    if request.method == "POST":
        form = CreateNewPost(request.POST)
        if form.is_valid():
            NewPost = form.save(commit=False)
            NewPost.author = request.user   # user is set as the author of the post
            NewPost.save()
            return HttpResponseRedirect(reverse("all_posts"))   # redirects to all_posts page
    postform = CreateNewPost()
    return render(request, "network/new_posts.html",{
        "form": postform,   # provides the form 
    })

def user_page(request, user_id):
    """This view renders the user profile page"""

    view_user = User.objects.get(id=user_id) # gets the user
    posts = NewPost.objects.filter(author=user_id) 
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/user_page.html", {
        "page_obj": page_obj, 
        "view_user": view_user,   # provides the username for the profile
        "followers": view_user.followers.all().count(), # provides the number of followers
        "following": view_user.following.all().count(), # provides the number users followed
        "follower_list": view_user.followers.all() # provides the list of followers (to check is the current user is already following)
    })


def follow(request, user_id):
    """This view adds the current user as a follower
     to an account when the follow button is clicked"""
    if request.method == "POST":
        try:
            user = User.objects.get(pk=user_id) # gets the user
        except User.DoesNotExist:
            raise Http404("User does not exist") 
        user.followers.add(request.user) 

    return HttpResponseRedirect(reverse("user_page", args = (user_id,) )) # redirects to the profile page


def unfollow(request, user_id):
    """This view removes the current user as a follower
     of an account when the unfollow button is clicked"""
    if request.method == "POST":
        try:
            user = User.objects.get(pk=user_id)  # gets the user
        except User.DoesNotExist:
            raise Http404("User does not exist")
        user.followers.remove(request.user)

    return HttpResponseRedirect(reverse("user_page", args = (user_id,) ))  # redirects to the profile page


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def like_post(request, user_id, post_id):
    """This view adds a like for the current user"""

    user = User.objects.get(id=user_id) # gets the user
    post = NewPost.objects.get(id=post_id)  # gets the post
    post.likes.add(user) # adds user's like to the post
    post.save()



def unlike_post(request, user_id, post_id):
    """This view removes the like for the current user"""

    user = User.objects.get(id=user_id) # gets the user
    post = NewPost.objects.get(id=post_id)  # gets the post
    post.likes.remove(user) # removes user's like from the post
    post.save()

# def edit_post(request, post_id): 
#     """This view edits a post"""
#     post = NewPost.objects.get(id=post_id)


