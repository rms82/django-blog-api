from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .permissions import IsOwner
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category

'''
function based view for API

@api_view()
def api_home(request):
    return Response(
        {
            'name': "reza",
        }
    )


@api_view(['GET', 'PUT', 'DELETE'])
def api_post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published=True)
    if request.method == 'GET':
        serializer = PostSerializer(post)

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()

        return Response(
            {
                'detail': "Post successfully deleted!!"
            },
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'POST'])
def api_post_list(request):
    if request.method == 'GET':
        posts = Post.objects.filter(published=True)
        serializer = PostSerializer(posts, many=True,)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

'''


'''
class based view with APIView for API


class ApiHome(APIView):
    def get(self, request):
        return Response(
            {
                'name': "reza",
            }
        )


class ApiPost(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(post)

        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk, published=True)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk, published=True)
        post.delete()

        return Response(
            {
                'detail': "Post successfully deleted!!"
            },
            status=status.HTTP_204_NO_CONTENT
        )


class ApiPostList(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
'''


'''
class based viwes with generics for API


class ApiPostList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()



class ApiPostCRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

'''


'''
class based viwes with ModelViewSet for APIs
'''


class ApiPost(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author', 'published',]
    search_fields = ['title', 'content']
    ordering_fields = ['published', 'created_date']

    @action(detail=False)
    def hello(self, request):
        return Response({
            'detail': 'Hi!!'
        })


class ApiCategory(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
