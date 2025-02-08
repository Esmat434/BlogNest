from django.shortcuts import redirect
from django.http import Http404, HttpResponseNotAllowed
from .models import Post
from accounts.models import CustomUser


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/signin/")
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not Post.objects.filter(id=pk, author=request.user).exists():
            return Http404(
                "Your permission is denied you are not the owner of this post"
            )
        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not CustomUser.objects.filter(
            username=request.user.username, is_superuser=True
        ).exists():
            return HttpResponseNotAllowed("you dont have permition to work on website!")
        return super().dispatch(request, *args, **kwargs)
