from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length = 100)
    fullname = models.CharField(max_length = 100)
    loggedIn = models.BooleanField(default=False)
    role = models.CharField(max_length = 100,default='user')
