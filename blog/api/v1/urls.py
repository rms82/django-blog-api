from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views
app_name = 'api'
router = DefaultRouter()
router.register('posts', views.ApiPost, basename='posts')
router.register('category', views.ApiCategory, basename='category')

# urlpatterns = [
    # path('', views.ApiHome.as_view(), name='api-home'),
    # path('posts/', views.ApiPostList.as_view(), name='api_post_list'),
    # path('posts/<int:pk>/', views.ApiPostCRUD.as_view(), name='api_post_detail'),

# ] 
urlpatterns = router.urls

