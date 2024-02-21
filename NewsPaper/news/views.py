from django.db.models.base import Model as Model
from config import settings
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Author, PostCategory
from .filters import PostsFilter
from .forms import PostForm

from django.core.cache import cache

from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .tasks import send_message

class PostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostsSearch(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        category_pk = request.POST['category']
        text = request.POST.get('text')
        title = request.POST.get('title')
        post_category = Category.objects.get(pk=category_pk)
        subscribers = post_category.subscribers.all()

        if form.is_valid():
            post = form.save(commit=False)
            post.rating = 0
            if self.request.path == 'news/articles/create/':
                post.position = 'AR'
            post.save()
        
        postcategory = PostCategory.objects.create(post=post, category=post_category)
        postcategory.save()

        for subscriber in subscribers:
            html_content = render_to_string(
                'mail.html', {'user': subscriber, 'text': text[:50], 'title': title, 'post': post}
            )
            # msg = EmailMultiAlternatives(
            #     subject=title,
            #     body=f"{text[:50]}",
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     to=[subscriber.email],
            # )
            # msg.attach_alternative(html_content, 'text/html')
            # msg.send()
            send_message(title, text, settings, subscriber, html_content)
        return redirect('/news/')
    

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'Post_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['is_not_subscribe'] = not self.request.user.category_set.filter(id=category.pk).exists()
        return context
    
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        author = Author.objects.create(user=user)
        author.save()
    return redirect('/news')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = "Вы успешно подписались на рассылку новостей категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})