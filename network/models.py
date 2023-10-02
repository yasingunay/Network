from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
   

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveBigIntegerField(default=0)
   

    def __str__(self):
        return f"Post by {self.user} at {self.timestamp}"


class Following(models.Model):
    """
    Model: Following - all who follows who info

    fields:
    * user - user who is following
    * user_followed - user who is being followed
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers" )



    def __str__(self):
        return f"{self.user} is following {self.user_followed}"

