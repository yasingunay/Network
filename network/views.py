from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

from django.contrib import messages
from .models import User, Post, Following


POST_NUMBER_PER_PAGE = 10


def index(request):
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, POST_NUMBER_PER_PAGE)  # Show2  contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "page_obj": page_obj
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
           
@login_required(login_url="/login")           
def following_view(request):
    # Get the user's followers
    user_following = request.user.following.all()
    # Extract the users being followed from the Following objects
    users_followed = [following.user_followed for following in user_following]
    # Filter posts by users being followed
    post_list = Post.objects.filter(user__in=users_followed).order_by('-timestamp')
    paginator = Paginator(post_list, POST_NUMBER_PER_PAGE)  # Show 10  contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "page_obj": page_obj
    })






@login_required(login_url="/login")  
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk = post_id)
        edit_post.content = data["content"]
        edit_post.save()
        test = "test123"

        response_data = {
            "message": "Change successful",
            "data": data["content"],
            "test": test
          
        }
        return JsonResponse(response_data)






