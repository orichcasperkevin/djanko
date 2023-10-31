from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class HankoProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hanko_id = models.CharField(max_length=48,unique=True)

    class Meta:
        unique_together = ('user','hanko_id')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        HankoProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(instance.hankoprofile)
    if hasattr(instance,'hankoprofile'):
        instance.hankoprofile.save()