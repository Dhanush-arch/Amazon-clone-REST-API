from django.db import models
from django.contrib.auth.models import User as defaultUser

class CustomUser(models.Model):
    userName = models.OneToOneField(defaultUser, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.userName)
