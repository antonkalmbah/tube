from django.db import models
from media_storage.models import Media
from django.contrib.auth.models import User


class Comment(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'Written {self.author.username} at {self.date_posted}'

    @property
    def current_rating(self):
        rating = CommentRating.objects.filter(comment=self)
        if len(rating) > 0:
            sum_rating = 0
            for element in rating:
                sum_rating += element.rating
            return sum_rating / len(rating)
        else:
            return 0


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()


class PrivatChat(models.Model):
    title = models.CharField(max_length=255)
    chat_users = models.ManyToManyField(User, related_name='chat_users')
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(PrivatChat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
