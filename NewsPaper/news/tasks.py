import time
import datetime

from django.core.mail import EmailMultiAlternatives, send_mail

from .models import Post
from config import settings
from config.celery import app


@app.task
def send_message(title, text, settings, subscriber, html_content):
    msg = EmailMultiAlternatives(
                subject=title,
                body=f"{text[:50]}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@app.task
def send_week():
    posts = Post.objects.filter(time_create__gt = datetime.datetime.now() - datetime.timedelta(days=7))
    category_posts = [post.category.all() for post in posts]
    subscribers = list()
    for categories in category_posts:
        for category in categories:
            for subscriber in category.subscribers.all():
                if subscriber not in subscribers:
                    subscribers.append(subscriber)
    titles = [post.title for post in posts]
    texts = [post.text[:50] for post in posts]
    send_mail(
        subject=titles,
        message=texts,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscriber.email for subscriber in subscribers],
        fail_silently=False
    )


