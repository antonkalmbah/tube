from django.contrib.auth.models import User
from django.db import models


class ProfileData(models.Model):
    username = models.ForeignKey(User, related_name='photo_owner', on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='img', max_length=254, blank=True)

    def __str__(self):
        return self.username.username

    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)


def get_name(self):
    return self.username


User.add_to_class("__str__", get_name)
