from django.contrib import admin
from .models import Comment, CommentRating, PrivatChat, Message

admin.site.register(Comment)
admin.site.register(CommentRating)
admin.site.register(PrivatChat)
admin.site.register(Message)
