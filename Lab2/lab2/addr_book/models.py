from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 30)
    qq = models.CharField(max_length = 30)
    renren = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
	