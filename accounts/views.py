import requests
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from .models import CustomUser, AccountVerified, PasswordForgotResetToken
from blog.models import Post, Follow
from .signupForm import SignupForm
from .send_mail import send_email
from .loggers import logger

# Create your views here.


class SignupView(View):
    def get(self, request):
        logger.info(
            f"requested from signup view to signupform for registration from app /accounts/views/SignupView."
        )
        form = SignupForm()
        context = {"form": form}
        logger.debug(
            "signup retrived successfully from app /accounts/views/SignupView."
        )
        return render(request, "Account/signup.html", context=context)

    def post(self, request):
        logger.info("Requested from signup post method for registration.")
        form = SignupForm(request.POST)

        if form.is_valid():
            user_data = self.get_cleaned_data(form)
            user = CustomUser.objects.create(**user_data)
            user.last_login_ip = self.get_client_ip(request)
            user.set_password(form.cleaned_data["password"])
            user.save()
            logger.debug(f"User {user.username} registered successfully.")
            return render(request, "Account/verify_account.html")

        # لاگ کردن خطاها
        logger.warning(f"Form is not valid. Errors: {form.errors}")
        return render(request, "Account/signup.html", {"form": form})

    def get_cleaned_data(self, form):
        cleaned_data = form.cleaned_data
        user_data = {
            "username": cleaned_data["username"],
            "first_name": cleaned_data["first_name"],
            "last_name": cleaned_data["last_name"],
            "picture": cleaned_data["picture"],
            "address1": cleaned_data["address1"],
            "address2": cleaned_data["address2"],
            "country": cleaned_data["country"],
            "city": cleaned_data["city"],
            "email": cleaned_data["email"],
            "phone_number": cleaned_data["phone_number"],
            "password": cleaned_data["password"],
            "birth_date": cleaned_data["birth_date"],
        }
        return user_data

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class SigninView(View):
    def get(self, request):
        logger.info(
            "requested from signin to login into your account from app /accounts/views/SigninView."
        )
        logger.debug(
            "request retrived successfully from app /accounts/views/SigninView."
        )
        return render(request, "Account/signin.html")

    def post(self, request):
        logger.info(
            "requested from signin post method to login in to your account from app /accounts/views/SigninView."
        )
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        user_exists = CustomUser.objects.filter(username=username).exists()
        if not user_exists:
            logger.warning(
                f"User: {username} does not exists with this username from app /accounts/views/SigninView."
            )
            return render(
                request, "Account/signin.html", {"error": "User does not exists."}
            )
        user = authenticate(request, username=username, password=password)
        if user:
            logger.debug(
                f"User: {username} with this username successfully exists and you loged into your account from app /accounts/views/SigninView."
            )
            if not self.checkLoginDeviceIp(request, user):
                login(request, user)
                return redirect(reverse("home"))
            else:
                login(request, user)
                return redirect(reverse("home"))
        logger.warning(
            f"User: {username} does not have an account or password is incorrect from app /accounts/views/SigninView."
        )
        return render(request, "Account/signin.html", {"error": "Incorrect password!"})

    def checkLoginDeviceIp(self, request, user):
        ip = self.get_client_ip(request)
        if ip != user.last_login_ip:
            confirmation_link = request.build_absolute_uri(
                reverse("Suspicious_Activity", args=[user.pk])
            )
            city, country = self.get_ip_location(ip)
            message = f"""<p>Hi {user.username}
                        <br/>
                        Someone just logged into your account from new device located in {city} : {country} if this was not you
                        <br/>  
                        <a href="{confirmation_link}">please click here to logout from account</a>
                        </p>"""
            send_email(message, user.email)
            user.last_login_ip = ip
            user.save()
            return True
        return False

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_ip_location(self, ip_address):
        url = f"https://ipinfo.io/{ip_address}/json?token=576ad8fcac7ba7"
        response = requests.get(url)
        information = response.json()
        city = information["city"] if "city" in information else None
        country = information["country"] if "country" in information else None
        return (city, country)


class Lock_Account_on_Suspicious_Activity_View(View):
    def get(self, request, pk):
        logger.info(
            "requested from confrim login if someone hacked your account you can logout from app /accounts/views/ConfirmLoginView."
        )
        try:
            user = CustomUser.objects.get(username=request.user.username, id=pk)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            logger.warning(
                "user with this primary key number does not have an account from app /accounts/views/ConfirmLoginView."
            )
            user = None
        if user:
            logger.debug(
                f"User: {user.username} will successfully logout from app /accounts/views/ConfirmLoginView."
            )
            logout(request)
            return redirect(reverse("signin"))
        else:
            return redirect(reverse("signin"))


class SignoutView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User: {request.user.username} requested successfully sended from app /accounts/views/SignouttView."
        )
        logger.debug(
            f"User: {request.user.username} retrived successfully from app /accounts/views/SignouttView."
        )
        return render(request, "Account/signout.html")

    def post(self, request):
        username = request.user.username
        logger.info(
            f"User: {username} signout successfully from app /accounts/views/SignouttView."
        )
        logout(request)
        logger.debug(
            f"User: {username} successfully signout from app /accounts/views/SignouttView."
        )
        return redirect(reverse("home"))


class AccountVerifiedView(View):
    def get(self, request, token):
        logger.info(
            "user requested successfully sended from app /accounts/views/AccountVerifiedtView."
        )
        try:
            user_verified = AccountVerified.objects.get(token=token)
        except AccountVerified.DoesNotExist:
            logger.warning(
                "user unretrived token does not exists from app /accounts/views/AccountVerifiedtView."
            )
            return HttpResponse("token does not exists")
        user_verified.user.email_verified = True
        user_verified.user.save()
        is_authenticate = authenticate(
            request,
            username=user_verified.user.username,
            password=user_verified.user.password1,
        )
        if is_authenticate:
            login(request, is_authenticate)
        else:
            logger.warning(
                f"User: {user_verified.user.username} unretrived you were not login from app /accounts/views/AccountVerifiedtView."
            )
        logger.debug(
            f"User: {user_verified.user.username} login successfully from app /accounts/views/AccountVerifiedtView."
        )
        user_verified.delete()
        return reverse("home")


class PasswordForgotResetView(View):
    def get(self, request, token):
        reset_token = self.get_token(token)
        if reset_token is None:
            return HttpResponse("Passwod Forgot Reset Token DoesNotExist")
        elif reset_token.is_expired:
            return HttpResponse("The reset link has expired. Please request a new one.")
        return render(request, "Account/passwordReset.html")

    def post(self, request, token):
        reset_token = self.get_token(token)
        if reset_token is None:
            return HttpResponse("Passwod Forgot Reset Token DoesNotExist")

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password == confirm_password:
            user = reset_token.user
            user.password = make_password(new_password)
            user.save()
            reset_token.delete()
            return redirect(reverse("signin"))
        return render(
            request, "Account/passwordForgot.html", {"error": "Passwords do not match."}
        )

    def get_token(self, token):
        try:
            reset_token = PasswordForgotResetToken.objects.get(token=token)
        except PasswordForgotResetToken.DoesNotExist:
            return None
        return reset_token


class PasswordForgotResetTokenView(View):
    def get(self, request):
        logger.info(
            "user requested successfully sneded from app /accounts/views/PasswordForgotView."
        )
        logger.debug(
            "user successfully retrived from app /accounts/views/PasswordForgotView."
        )
        return render(request, "Account/passwordForgot.html")

    def post(self, request):
        logger.info(
            "user requested successfully from app /accounts/views/PasswordForgotView."
        )

        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            logger.warning(
                "user unretrived your emial is not correct or you dont have an account."
            )
            return render(
                request,
                "Account/message.html",
                {"message": "Please check your email to get your password"},
            )

        if PasswordForgotResetToken.objects.filter(user=user).exists():
            PasswordForgotResetToken.objects.get(user=user).delete()

        reset_token = PasswordForgotResetToken.objects.create(user=user)
        link = f'<a href="http://127.0.0.1:8000/password-forgot/{reset_token.token}/">Click here to set yout password</a>'

        send_email(link, user.email)

        logger.debug(
            f"User: {user.username} retrived successffully to change her password from app /accounts/views/PasswordForgotView."
        )
        return render(
            request,
            "Account/message.html",
            {"message": "Please check your email to get your password"},
        )


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"user: {request.user.username} requested successfully from app /accounts/views/ProfiletView."
        )

        try:
            user = CustomUser.objects.get(username=request.user.username)
        except CustomUser.DoesNotExist:
            logger.warning(
                "this yourname does not exists you dont have an account from app /accounts/views/ProfiletView."
            )
            return redirect(reverse("signin"))

        total_posts, total_followers = self.get_report(request)

        logger.debug(
            f"User: {user.username} retrived successfuly view their site from app /accounts/views/ProfiletView."
        )
        return render(
            request,
            "Account/profile.html",
            {
                "user": user,
                "total_posts": total_posts,
                "total_followers": total_followers,
            },
        )

    def get_report(self, request):
        posts = Post.objects.filter(author=request.user).annotate(
            comment_count=Count("Comment"), total_likes=Sum("likes")
        )
        followers = Follow.objects.filter(followee=request.user)
        return posts, followers


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User: {request.user.username} requested successfully sended from app /accounts/views/ProfileEditView."
        )
        try:
            user = CustomUser.objects.get(username=request.user.username)
        except CustomUser.DoesNotExist:
            logger.warning(
                "User dont have an account from app /accounts/views/ProfileEditView."
            )
            return redirect(reverse("signin"))
        logger.debug(
            f"User: {request.user.username} retrive successfully from app /accounts/views/ProfileEditView."
        )
        return render(request, "Account/profileEdit.html", {"user": user})

    def post(self, request):
        logger.info(
            f"User: {request.user.username} requested successfully from app /accounts/views/ProfileEditView."
        )
        data = request.POST
        picture = request.FILES.get("picture")

        try:
            user = CustomUser.objects.get(username=request.user.username)
        except CustomUser.DoesNotExist:
            logger.warning(
                "you dont have an account from app /accounts/views/ProfileEditView."
            )
            return redirect(reverse("signin"))
        logger.debug(
            f"User: {user.username} retrived successfully from app /accounts/views/ProfileEditView."
        )
        # Update user data
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.address1 = data.get("address1", user.address1)
        user.address2 = data.get("address2", user.address2)
        user.country = data.get("country", user.country)
        user.city = data.get("city", user.city)
        user.birth_date = data.get("birth_date", user.birth_date)

        # Update picture if provided
        if picture:
            user.picture = picture

        # Check and update password
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 and password2:
            if password1 != password2:
                return render(
                    request,
                    "Account/profileEdit.html",
                    {"user": user, "error": "Passwords do not match"},
                )
            user.set_password(password1)
        user.save()
        return redirect(reverse("profile"))


class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User : {request.user.username} requesded successfully sended from app /accounts/views/DeleteAccountView."
        )
        logger.debug(
            f"User: {request.user.username} retrived successfully from app /accounts/views/DeleteAccountView."
        )
        return render(request, "Account/deleteAccount.html")

    def post(self, request):
        logger.info(
            f"User: {request.user.username} requested successfully from app /accounts/views/DeleteAccountView."
        )
        try:
            user = CustomUser.objects.get(username=request.user.username)
        except CustomUser.DoesNotExist:
            logger.warning(
                f"User: {request.user.username} mabay does not have an account from app /accounts/views/DeleteAccountView."
            )
            return redirect(reverse("signin"))
        logger.debug(
            f"User: {user.username} retrived successfully deleted from app /accounts/views/DeleteAccountView."
        )
        user.delete()
        return redirect(reverse("home"))


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        return render(request, "Account/settings.html", {"user": user})

    def post(self, request):
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        try:
            user = CustomUser.objects.get(
                username=request.user.username, password=current_password
            )
        except CustomUser.DoesNotExist:
            return HttpResponse("not found")

        if new_password != confirm_password:
            return redirect("/settings/")
        user.set_password(new_password)
        user.save()
        return redirect(reverse("dashboard"))
