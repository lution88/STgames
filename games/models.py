from django.db import models
from user.models import UserModel



# Create your models here.
class Games(models.Model):
    class Meta:
        db_table = "games"

    game_num = models.BigAutoField(primary_key=True)
    game = models.CharField(max_length=256)
    playtime = models.CharField(max_length=256)
    user_id = models.ForeignKey( UserModel , on_delete=models.CASCADE ,db_column='user_code')
