from rest_framework import serializers
from .models import Comment, Message, PrivatChat, CommentRating


class PrivateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivatChat
        fields = ('id', 'title', 'chat_users', 'date_created', 'description')
        extra_kwargs = {
                        'chat_users': {'required': False},
                        }
        lookup_field = 'title'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'author', 'chat', 'date_posted', 'content',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'media', 'author', 'date_posted', 'current_rating', 'content')
        extra_kwargs = {'author': {'required': False}, }


class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentRating
        fields = ('id', 'comment', 'author', 'rating')
