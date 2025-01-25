import random
from itertools import chain

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import FollowerCount, LikePost, Post, Profile

from auto_caption.utils import create_caption


@login_required(login_url="signin")
def index(request):
    user = request.user
    print(user)
    profile = Profile.objects.get(user=user)

    posts = Post.objects.all()

    posts_profiles = []
    user_following_list = []
    feed = []

    user_following = FollowerCount.objects.filter(follower=request.user.username)

    for following in user_following:
        user_following_list.append(following.user)

    for username in user_following_list:
        following_posts = Post.objects.filter(user=username)
        feed.append(following_posts)

    # The * in chain(*feed) is the unpacking operator in Python.
    # Its purpose is to unpack the elements of an iterable (such as a list or tuple)
    # so that each element is passed as a separate argument to the function.
    feed_list = sorted(chain(*feed), key=lambda post: post.created_at, reverse=True)

    for post in feed_list:
        post_user = User.objects.get(username=post.user)
        post_profile = Profile.objects.get(user=post_user)
        posts_profiles.append({"post": post, "profile": post_profile})

    # User suggestion
    all_users = User.objects.all()
    user_following_all = FollowerCount.objects.filter(follower=user.username)

    following_list = []

    for user in user_following_all:
        following_list.append(User.objects.get(username=user.user))

    suggestion_list = [user for user in all_users if user not in following_list]

    random.shuffle(suggestion_list)

    user_profile_list = []
    for user in suggestion_list:
        the_user = User.objects.get(username=user)
        try:
            the_profile = Profile.objects.get(user=the_user)
            user_profile_list.append(
                {"username": user.username, "profile": the_profile}
            )
        except Exception as e:
            continue

    return render(
        request=request,
        template_name="index.html",
        context={
            "user_profile": profile,
            "posts": feed_list,
            "posts_profiles": posts_profiles,
            "user_profile_list": user_profile_list,
        },
    )


def signup(request):
    if request.method == "POST":
        # print(request.POST)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            messages.info(request=request, message="Password Not Matching!")
            return redirect("signup")
        elif User.objects.filter(email=email).exists():
            messages.info(request=request, message="Email Address is Already in Use!")
            return redirect("signup")
        elif User.objects.filter(username=username).exists():
            messages.info(request=request, message="Username is Already in Use!")
            return redirect("signup")
        else:
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            new_user.save()

            new_user_login = auth.authenticate(username=username, password=password)
            auth.login(request=request, user=new_user_login)

            the_user = User.objects.get(username=username)

            new_profile = Profile.objects.create(user=the_user, id_user=the_user.id)
            new_profile.save()

            # Each user is a follower of itself
            temp = FollowerCount.objects.create(
                user=the_user.username, follower=the_user.username
            )
            temp.save()

            return redirect("settings")
    else:
        return render(request=request, template_name="signup.html")


def signin(request):
    # print(request.POST)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request=request, user=user)
            return redirect(request=request, to="/")
        else:
            messages.info(request=request, message="Invalid Credentials!")
            return redirect("signin")
    else:
        return render(request=request, template_name="signin.html")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request=request)
    return redirect("signin")


@login_required(login_url="signin")
def settings(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":

        if request.FILES.get("image") == None:
            image = user_profile.profile_image
            bio = request.POST["bio"]
            location = request.POST["location"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            user.first_name = first_name
            user.last_name = last_name
            user.save()

        elif request.FILES.get("image"):
            image = request.FILES["image"]
            bio = request.POST["bio"]
            location = request.POST["location"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            user.first_name = first_name
            user.last_name = last_name
            user.save()

        return redirect("settings")

    return render(
        request=request,
        template_name="setting.html",
        context={"user_profile": user_profile},
    )


@login_required(login_url="signin")
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES["image_upload"]
        auto_caption = request.POST.get("auto_caption")

        if auto_caption:  # Generate a caption if the checkbox is checked
            caption = create_caption(image).capitalize()
        else:
            caption = request.POST["caption"]

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect("/")

    else:
        return redirect("/")

# @login_required(login_url="signin")
# def like_post(request):
#     username = request.user.username
#     post_id = request.GET["post_id"]

#     like = LikePost.objects.filter(post_id=post_id, username=username).first()

#     if not like:
#         new_like = LikePost.objects.create(post_id=post_id, username=username)
#         new_like.save()

#         number_of_likes = Post.objects.get(id=post_id).number_of_likes
#         number_of_likes += 1
#         Post.objects.filter(id=post_id).update(number_of_likes=number_of_likes)

#         return redirect("/")
#     else:
#         like.delete()
#         number_of_likes = Post.objects.get(id=post_id).number_of_likes
#         number_of_likes -= 1
#         Post.objects.filter(id=post_id).update(number_of_likes=number_of_likes)

#         return redirect("/")

import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="signin")
@csrf_exempt
def like_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_id = data.get("post_id")
            post = get_object_or_404(Post, id=post_id)
            username = request.user.username
            likes = LikePost.objects.filter(post_id=post_id, username=username).first()

            if not likes:
                action = "liked"

                new_like = LikePost.objects.create(post_id=post_id, username=username)
                new_like.save()

                number_of_likes = post.number_of_likes
                number_of_likes += 1
                post.number_of_likes = number_of_likes
                post.save()
            else:
                action = "unliked"

                likes.delete()

                number_of_likes = post.number_of_likes
                number_of_likes -= 1
                post.number_of_likes = number_of_likes
                post.save()

            # Return the updated number of likes
            return JsonResponse(
                {
                    "success": True,
                    "number_of_likes": post.number_of_likes,
                    "action": action,
                }
            )

        except Post.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Post not found"}, status=404
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required(login_url="signin")
def profile(request, pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=pk)
    number_of_posts = len(posts)
    # followers = FollowerCount.objects.filter(user=pk)

    if FollowerCount.objects.filter(follower=request.user.username, user=pk).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    user_followers = FollowerCount.objects.filter(user=pk)
    number_of_user_followers = len(user_followers) - 1

    user_following = FollowerCount.objects.filter(follower=pk)
    number_of_user_following = len(user_following) - 1

    context = {
        "user_object": user,
        "profile_object": profile,
        "posts": posts,
        "number_of_posts": number_of_posts,
        "button_text": button_text,
        "number_of_user_followers": number_of_user_followers,
        "number_of_user_following": number_of_user_following,
    }

    return render(request=request, template_name="profile.html", context=context)


@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]

        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delete_follow = FollowerCount.objects.get(follower=follower, user=user)
            delete_follow.delete()
            return redirect(f"/profile/{user}")
        else:
            new_follower = FollowerCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect(f"/profile/{user}")

    else:
        return redirect("/")


@login_required(login_url="signin")
def search(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)

    searched_profiles = []

    if request.method == "POST":
        username = request.POST["username"]
        searched_user = User.objects.filter(username__icontains=username)

        for user in searched_user:
            temp = User.objects.get(username=user.username)
            profile = Profile.objects.get(user=temp)
            searched_profiles.append(profile)

    return render(
        request=request,
        template_name="search.html",
        context={
            "user_profile": user_profile,
            "username_profile_list": searched_profiles,
        },
    )
