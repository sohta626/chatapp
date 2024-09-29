from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django import forms
# Create your models here.

class User(AbstractUser):
    
    email = models.EmailField(_("email address"), unique=True)
    img = models.ImageField()
    def __str__(self):
        return self.username


class Talk(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    message = models.TextField()
    send_time = models.DateTimeField()
