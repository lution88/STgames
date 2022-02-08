from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'

    nickname = models.CharField(max_length=256, default='')
    pro_img_url = models.CharField(max_length=256, default='')


class Games(models.Model):
    class Meta:
        db_table = 'games'

    game = models.CharField(max_length=256, default='')
    tag = models.CharField(max_length=256, default='')
    game_id = models.CharField(max_length=256, default='')
    game_url = models.CharField(max_length=256, default='')


class FavoriteGames(models.Model):
    class Meta:
        db_table = 'favoritegames'

    game_id = models.CharField(max_length=256, default='')
    user_id = models.CharField(max_length=256, default='')
    playtime = models.DateTimeField(blank=True, null=True)


class RecommendGames(models.Model):
    class Meta:
        db_table = 'recommendgames'

    user_id = models.IntegerField(null=True)
    rec_game = models.TextField(default='')


class SimilarUser(models.Model):
    class Meta:
        db_table = 'similarusers'

    sim_user = models.CharField(max_length=50, default='')
    sim_game_list = models.TextField(default='')