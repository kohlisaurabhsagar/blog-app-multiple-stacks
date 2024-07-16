from rest_framework import serializers
from .models import PostModel, Comments

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author_username', 'post', 'content']
        read_only_fields = ['author_username', 'post']


class PostModelSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)  

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'image', 'user_username', 'date_created', 'comments']
        read_only_fields = ['user_username']
