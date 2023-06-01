from django.urls import path, include

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('google/', views.Google.as_view(), name='google'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('api/v1/', include('blog.api.v1.urls')),

]
