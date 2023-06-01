from django.db import models

from django.shortcuts import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    content = models.TextField()
    category = models.ManyToManyField(Category)
    published = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})
    
    def get_api_absolute_url(self):
        return reverse("blog:api:posts-detail", kwargs={"pk": self.pk})

    def get_snippet(self):
        if len(self.content) <= 5:
            return self.content
        
        return self.content[0:5] + '...'


    