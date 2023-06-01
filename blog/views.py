from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post
from .forms import PostForm

# Create your views here.


class Home(TemplateView):
    template_name = 'home.html'


class Google(RedirectView):
    url = 'https://google.com'


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(published=True)


class PostDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = ('blog.view_post', )
    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'published', 'published_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post_list")
