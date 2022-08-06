from django.db import models
from django.contrib.auth.models import User


class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    media = models.FileField(upload_to='content/%Y/%m/%d/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField()

    def __str__(self):
        return f'{self.title} by {self.author.username} at {self.date_posted}'

    def delete(self, *args, **kwargs):
        self.media.delete()
        super().delete(*args, **kwargs)

    @property
    def current_rating(self):
        rating = MediaRating.objects.filter(media=self)
        if len(rating) > 0:
            sum_rating = 0
            for element in rating:
                sum_rating += element.rating
            return sum_rating / len(rating)
        else:
            return 0


class MediaRating(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
