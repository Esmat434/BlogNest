from django.contrib import admin
from .models import Chat, ChatGroupToken

# Register your models here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_time"]


@admin.register(ChatGroupToken)
class ChatGroupTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "token", "created_time"]
