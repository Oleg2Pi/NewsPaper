from django.db import models
from django.contrib.auth.models import User
from news.recourse import POSITIONS, news
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_news = self.post_set.all().aggregate(Sum('rating'))['rating__sum']
        rating_user = self.user.comment_set.all().aggregate(Sum('rating'))['rating__sum']
        rating_comment = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_news * 3 + rating_user + rating_comment
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def get_absolute_url(self):
        return reverse(
            'news:category_detail',
            args=[self.id]
        )
    
    def get_post(self):
        return self.post_set.all()
    
    
class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'
    
    def get_absolute_url(self):
        return reverse(
            'news:post_detail', 
            args=[self.id]
            )
    
    def get_category(self):
        categories = self.category.all()
        if len(categories) == 1:
            return f"{categories[0].name}"
        else:
            list_category = []
            for category in categories:
                list_category.append(category.name)
            return f"{', '.join(list_category)}"
        
    def get_category_url(self):
        category = self.category.all()[0]
        return reverse(
            'news:category_detail',
            args=[category.id]
        )


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
