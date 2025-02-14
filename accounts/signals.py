import os
from django.db.models.signals import post_save, pre_delete
from django.utils.crypto import get_random_string
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from .models import CustomUser, Profile, AccountVerified
from .send_mail import send_email


def create_random_password_and_send_email(user):
    password = get_random_string(length=10)
    user.password1 = password
    user.save()
    message = f"""<p>This is your account Password Please save this password and dont forget
                <br/>
                Password: <span style="fint-size:30px">{password}</span>
                </p>"""
    send_email(message, user.email)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.socialaccount_set.exists():
            with transaction.atomic():
                create_random_password_and_send_email(instance)
        with transaction.atomic():
            AccountVerified.objects.create(user=instance)
            Profile.objects.create(user=instance)


@receiver(pre_delete, sender=CustomUser)
def delete_data_user(sender, instance, **kwargs):
    if instance.picture and instance.pucture.path:
        file_path = f"{instance.picture.path}"
        if os.path.exists(file_path):
            os.remove(file_path)


@receiver(post_save, sender=AccountVerified)
def send_token_to_email(sender, instance, created, **kwargs):
    if created:
        try:
            link = f'<p><a href="http://127.0.0.1:8000/account-verified/{instance.token}/">Click here to activate</a></p>'
            send_email(link, instance.user.email)
        except Exception as e:
            print(f"Error sending email: {e}")


@receiver(user_logged_in)
def handle_google_login(sender, request, user, **kwargs):
    if user.socialaccount_set.exists():
        create_random_password_and_send_email(user)
