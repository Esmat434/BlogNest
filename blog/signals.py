import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import transaction
from django.db.models import Prefetch
from .models import Post, PostVideo, PostImage


@receiver(pre_delete, sender=Post)
def delete_data_post(sender, instance, **kwargs):
    try:
        post = Post.objects.prefetch_related(Prefetch("image"), Prefetch("video")).get(
            id=instance.id
        )
        if post.image.exists():
            for image in post.image.all():
                file_path = image.image.path
                if os.path.isfile(file_path):
                    os.remove(file_path)
        if post.video.exists():
            for video in post.video.all():
                file_path = video.video.path
                if os.path.isfile(file_path):
                    os.remove(file_path)
    except Post.DoesNotExist:
        pass


@receiver(pre_delete, sender=PostImage)
def delete_image_data(sender, instance, **kwargs):
    if instance.image and instance.image.path:
        file_path = f"{instance.image.path}"
        if os.path.exists(file_path):
            os.remove(file_path)


@receiver(pre_delete, sender=PostVideo)
def delete_video_data(sender, instance, **kwargs):
    if instance.video and instance.video.path:
        file_path = f"{instance.video.path}"
        if os.path.exists(file_path):
            os.remove(file_path)
