from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:signin"))
        return super().dispatch(request, *args, **kwargs)
