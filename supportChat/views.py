from django.shortcuts import render
from django.views import View
from .mixin import LoginRequiredMixin

# Create your views here.

class ChatView(LoginRequiredMixin, View):
    def get(self, request, username, token):
        return render(request, "Chat/chat.html", {"username": username, "token": token})
