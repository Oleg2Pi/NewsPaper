from django.contrib import admin
from .models import Author, Post, Comment, Category, PostCategory, CategorySubscribers
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

admin.site.register(Author)


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post)
admin.site.register(Comment)


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(CategorySubscribers)
