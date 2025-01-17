from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def followers(self):
        return Follow.objects.filter(following=self)

    def following(self):
        return Follow.objects.filter(follower=self)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.follower} follows {self.following}"
    class Meta:
        unique_together = ('follower', 'following') #must be unique together

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    def serialize(self):
        return {
            "id": self.id,  
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count()
        }
    
    def CurTime(self):
        return self.timestamp.toLocaleString()
    def __str__(self):
        return f"{self.user}: {self.content[:50]}"

