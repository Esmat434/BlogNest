from django.db import models
from accounts.models import CustomUser
import uuid

# Create your models here.


class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)


class ChatGroupToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)
