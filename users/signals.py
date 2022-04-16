from django.contrib.auth import get_user_model
from django.dispatch import receiver, Signal

from django.db.models.signals import post_save
from store.signals import order_placed
from . import models


@receiver(order_placed)
def send_email(sender, **kwargs):
    print("order placed")


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)
    instance.profile.save()
