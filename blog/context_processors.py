from .models import Follow
from accounts.models import CustomUser


def total_follow_in_navbar(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
    except CustomUser.DoesNotExist:
        user = None

    if request.user.is_authenticated:
        total_followee = Follow.objects.filter(follower=request.user).count()
        return {"total_followee": total_followee, "user": user}
    return {"total_followee": 0, "user": user}
