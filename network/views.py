from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.contrib import messages
from .models import User, Post, Following


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html",{
        "posts": posts
    })


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

@login_required(login_url="/login")
def new_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content: 
            post = Post(user=request.user, content=content)
            post.save()
            return HttpResponseRedirect(reverse("index"))
   
@login_required(login_url="/login")
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get the User object with the specified user_id
    if request.method == "GET":
        posts = Post.objects.filter(user=user)  # Filter posts for the specific user
        is_following = Following.objects.filter(user=request.user, user_followed=user_id).exists()
        return render(request, "network/profile.html",{
            "posts" : posts,
            "user": user,
            "is_following": is_following
        })
    if request.method == "POST":
        if 'follow' in request.POST:
            if user != request.user:
                new_following = Following(user = request.user, user_followed = user)
                new_following.save()
                messages.success(request, f"You are now following {user.username}")
        elif 'unfollow' in request.POST:
            if user != request.user:
               Following.objects.filter(user = request.user, user_followed = user).delete()
               messages.success(request, f"You have unfollowed {user.username}")
    
    return redirect('profile', user_id=user_id)
           
            


