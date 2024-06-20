from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from .models import User,Post,Follow
from django import forms
import json
class NewPostForm(forms.Form):
    content = forms.CharField(
            label="New Post",
            widget=forms.Textarea(attrs={'rows': 5, 'cols': 50})
        )
def index(request):
    postForm =  NewPostForm()
    posts = Post.objects.all().order_by("-timestamp")

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    if request.user.is_authenticated:
        return render(request, "network/index.html", {
            "pages": posts,
            "postForm": postForm
        })
    return render(request, "network/index.html",{
        "posts": posts
    
    })

def GetUser(request,user):
    is_following = Follow.objects.filter(follower=request.user.id,following=User.objects.get(username=user).id).exists()  
    is_user = False
    if User.objects.get(username=user).id == request.user.id:
        is_user = True
    print(is_user)
    userOb = User.objects.get(username=user)
    followers = Follow.objects.filter(following=userOb.id).count()
    following = Follow.objects.filter(follower=userOb.id).count()
    posts = User.objects.get(username=user).posts.all().order_by("-timestamp")
    post_count = posts.count()
    # need a number of posts per page 
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/userprofile.html",{
        "pages": posts,
        "post_count": post_count,
        "followers": followers,
        "following": following,
        "username": user,
        "is_following": is_following,
        "is_user": is_user  
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




@login_required(login_url='/login')
def NewPost(request):
    postForm = NewPostForm()
    if request.method == "POST":
        postForm = NewPostForm(request.POST)
        if postForm.is_valid():
            content = postForm.cleaned_data["content"]
            post = Post(user=request.user, content=content)
            post.save()
            print(post)
            return HttpResponseRedirect(reverse("index"))
    
def FollowUser(request,username):
    # do not allow a user to follow themselves
    if User.objects.get(username=username).id == request.user.id: 
        return HttpResponseRedirect(reverse("userprofile",args=(username,)))
    if request.method == "POST":
        if Follow.objects.filter(follower=request.user.id,following=User.objects.get(username=username).id).exists():
            Follow.objects.filter(follower=request.user.id,following=User.objects.get(username=username).id).delete()
        else:
            follow = Follow(follower=request.user,following=User.objects.get(username=username))
            follow.save()
    return HttpResponseRedirect(reverse("userprofile",args=(username,)))

@login_required(login_url='/login')
def FollowingPage(request):
    following = Follow.objects.filter(follower=request.user.id)
    following_users = [follow.following for follow in following]
    post = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    # need a number of posts per page 
    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/followingpost.html",{
        "posts": post,
        "pages": posts
     
    })

@login_required(login_url='/login')
def LikePost(request,post_id):
    print("like")
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
            return JsonResponse({"likes": post.likes.count(),"liked": False})
        else:
            post.likes.add(request.user)
            post.save()
            return JsonResponse({"likes": post.likes.count(),"liked": True})
        
    
@login_required(login_url='/login')
def EditPost(request,post_id):
    print("edit")
    post = get_object_or_404(Post, id=post_id)
    print(post)
    if post.user != request.user:
        print("not allowed")
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "POST":
        data = json.loads(request.body)
        postForm = NewPostForm(data)
        if postForm.is_valid():
            content = postForm.cleaned_data["content"]
            post.content = content
            post.save()
            print("saved")
            return JsonResponse({"content": post.content})
   
    return HttpResponseRedirect(reverse("index"))