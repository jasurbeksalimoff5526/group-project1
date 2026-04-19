from django.contrib.auth.models import AbstractUser
from django.db import models
from shared.models import BaseModel

class CustomUser(BaseModel, AbstractUser):
    email = models.EmailField(unique=True) 
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True
    )
    bio = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Notification(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} — {self.text[:40]}"

    class Meta:
        ordering = ['-created_at']
