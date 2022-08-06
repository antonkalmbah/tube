import json
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import get_user_model

from accounts.permissions import IsOwnerOrReadOnly

from .serializers import CommentSerializer, CommentRatingSerializer, MessageSerializer, PrivateChatSerializer
from .models import Comment, CommentRating, PrivatChat, Message


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = ['media']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRatingViewSet(viewsets.ModelViewSet):
    queryset = CommentRating.objects.all()
    serializer_class = CommentRatingSerializer


class PrivateChatJoinAPIView(APIView):
    permissions_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return PrivatChat.objects.get(pk=pk)
        except PrivatChat.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        chat = self.get_object(pk)
        messages = Message.objects.filter(chat__id=pk)
        if request.user in chat.chat_users.all():
            pass
        else:
            chat.chat_users.add(request.user)

        list_of_message = []
        for item in messages:
            dict_message = {'author': item.author.username, 'author_id': item.author.pk,
                            'date_posted': item.date_posted.strftime("%d-%m-%Y %H:%M:%S"), 'content': item.content}
            list_of_message.append(dict_message)

        list_members = []
        for usr in chat.chat_users.all():
            list_members.append({'id': usr.id, 'username': usr.username})

        dict_response = {'chat': pk, 'title': chat.title, 'chat_users': list_members, 'messages': list_of_message}

        return Response(dict_response)


class PrivateChatViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    queryset = PrivatChat.objects.all()
    serializer_class = PrivateChatSerializer

    def perform_create(self, serializer):
        str_data = json.dumps(self.request.data)
        data = json.loads(str_data)
        first_member_list = []
        users = get_user_model()
        for userID in data['chat_users']:
            first_member_list.append(users.objects.get(pk=int(userID)))
        serializer.save(chat_users=first_member_list)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['chat']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
