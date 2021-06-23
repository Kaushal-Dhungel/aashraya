from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,email = instance.email)

@receiver(post_save, sender=Profile)
def post_save_update_profile(sender, instance, created, **kwargs):
    user = instance.user

    if created == False:
        user.email = instance.email
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.save()