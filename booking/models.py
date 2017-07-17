from django.db import models

# django database to store details about user that will be obtained from the MySQL database

class UserInfo(models.Model):
    username = models.CharField(max_length = 100)
    fullname = models.CharField(max_length = 100)
    loggedIn = models.BooleanField(default=False)
    role = models.CharField(max_length = 100,default='user')
