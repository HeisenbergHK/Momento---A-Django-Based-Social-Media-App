from django.urls import path

from .views import index, like_post, logout, profile, settings, signin, signup, upload, delete, follow, search

urlpatterns = [
    path("", view=index, name="index"),
    path("signup/", view=signup, name="signup"),
    path("signin/", view=signin, name="signin"),
    path("logout/", view=logout, name="logout"),
    path("setting/", view=settings, name="settings"),
    path("upload/", view=upload, name="upload"),
    path("delete/<uuid:pk>", view=delete, name="delete"),
    path("like-post", view=like_post, name="like-post"),
    path("profile/<str:pk>", view=profile, name="profile"),
    path("follow", view=follow, name="follow"),
    path("search", view=search, name="search"),
]
