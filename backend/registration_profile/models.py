import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def code_generator(length=5):
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


User = get_user_model()


class RegistrationProfile(models.Model):
    status_choices = [
        (1, 'Inactive'),
        (2, 'Activated')
    ]

    code = models.IntegerField(default=code_generator)
    email = models.EmailField(max_length=400, blank=True, null=True)
    status = models.IntegerField(choices=status_choices, default=1)

    def __str__(self):
        return f'ID {self.id}: Registration profile from {self.email}'

    @receiver(post_save, sender=User)
    def create_registration_profile(sender, instance, **kwargs):
        profile = RegistrationProfile.objects.get(email=instance.email)
        profile.status = 2
        profile.save()
