from csv import unregister_dialect
from django.db import models

# Create your models here.

class UserModel(models.Model):
    class Meta:
        db_table = "user"
    
    user_code = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50)
    pro_img_url = models.CharField(max_length=255)
    play_game = models.CharField(max_length=255)

    def __str__(self):
        return self.user_id

