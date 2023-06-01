from rest_framework import serializers
from accounts.models import CustomUser, Profile

from ...models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    category = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Category.objects.all())
    url = serializers.ReadOnlyField(source='get_api_absolute_url')
    # category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'content', 'snippet', 'image','published',
                  'category', 'created_date', 'updated_date', 'published_date', 'url']
        read_only_fields = ['author',]
        

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')

        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)

        else:
            rep.pop('published_date', None)
            rep.pop('content', None)
            rep.pop('created_date', None)
            rep.pop('url', None)

        return rep  

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id=self.context.get('request').user.id)

        return super().create(validated_data)
