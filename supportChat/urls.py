from django.urls import path
from .views import ChatView

urlpatterns = [
    path("chat/<str:username>/<uuid:token>/", ChatView.as_view(), name="chat_view")
]
