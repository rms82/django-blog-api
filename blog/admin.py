from django.contrib import admin

from .models import Post, Category

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['title', 'published', ]
    ordering = ('-published', 'title')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)