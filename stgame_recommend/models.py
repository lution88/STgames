from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'

    nickname = models.CharField(max_length=256, default='')


class Games(models.Model):
    class Meta:
        db_table = 'games'

    game = models.CharField(max_length=256, default='')
    user_id = models.CharField(max_length=256, default='')
    playtime = models.DateTimeField(blank=True, null=True)
