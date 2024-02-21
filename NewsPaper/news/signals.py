from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post
from config import settings

@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    if created:
        subject = f"{instance.title}"
    else:
        subject = f'Post changed for {instance.author} {instance.time_create.date()}'
    category_list = instance.category.all()
    subscribers_list = []
    for category in category_list:
        for subscriber in category.subscribers.all():
            subscribers_list.append(subscriber)
    send_mail(
        subject=subject,
        message=instance.text[:50],
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscriber.email for subscriber in subscribers_list],
        fail_silently=False
    )