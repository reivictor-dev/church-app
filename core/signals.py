from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Posts


@receiver(pre_save, sender=Posts)
def posts_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)
