from supportChat.models import ChatGroupToken


def get_username_and_chat_access_token(request):
    if request.user.is_authenticated:
        access_token = ChatGroupToken.objects.get(id=1)
        return {"username": request.user.username, "access_token": access_token.token}
    else:
        return {"username":'UnKnown','access_token':0}
