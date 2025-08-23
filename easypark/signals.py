from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .detection_service import start_detection_in_background

@receiver(post_migrate)
def start_detection(sender, **kwargs):
    start_detection_in_background()
