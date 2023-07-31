from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Utilisateur

@receiver(post_save, sender=Utilisateur)
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:
        user_group, _ = Group.objects.get_or_create(name='Utilisateurs')
        instance.groups.add(user_group)
