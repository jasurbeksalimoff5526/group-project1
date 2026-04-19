from django.db import models
from django.conf import settings
from shared.models import BaseModel
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', 'Like'),
        ('LOVE', 'Love'),
        ('FIRE', 'Fire'),
        ('WOW', 'Wow'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    type = models.CharField(max_length=10, choices=REACTION_CHOICES)

class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=255)

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
