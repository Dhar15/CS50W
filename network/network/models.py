from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    post = models.CharField(max_length=255)
    timestamp =  models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "likes":self.likes,
            "is_liked": self.is_liked
        }

    def __str__(self):
        return f"{self.user} posted {self.post} at {self.timestamp} and has {self.likes} likes"

class Follow(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="liked_user")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_liked")

    def __str__(self):
        return f"Liked {self.post} post of {self.user}"
