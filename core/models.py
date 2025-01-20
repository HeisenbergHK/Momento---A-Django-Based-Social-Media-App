from django.contrib.auth import get_user_model
from django.db import models
import uuid
from datetime import datetime

# This is a model too.
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length=1000, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images", default="default-profile-picture.jpg"
    )
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    number_of_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.follower} follows {self.user}"
