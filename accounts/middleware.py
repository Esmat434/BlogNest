from django.shortcuts import HttpResponseRedirect
from django.utils.timezone import now
from django.conf import settings
from django.core.exceptions import PermissionDenied


def check_activity(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")
            current_time = now().timestamp()
            if last_activity and current_time - last_activity > 604800:
                request.session.flush()
                return HttpResponseRedirect("/login/")
            request.session["last_activity"] = current_time
        return get_response(request)

    return middleware
